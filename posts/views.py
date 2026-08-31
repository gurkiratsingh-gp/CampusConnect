import csv

from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from .ai_classifier import predict_category
from .forms import CommentForm, EventForm, LostFoundItemForm, PostForm, ProfileForm, ReportForm, SignUpForm
from .models import Bookmark, Comment, Community, Event, Like, LostFoundItem, Notification, Post, Profile, Report, RSVP


def home(request):
    categories = ["Academic", "Placement", "Event", "Marketplace", "Lost & Found", "General"]
    selected_category = request.GET.get("category", "")
    posts = Post.objects.order_by("-created_at")

    if selected_category in categories:
        posts = posts.filter(ai_category=selected_category)
    else:
        selected_category = ""

    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "posts/home.html",
        {
            "posts": page_obj,
            "page_obj": page_obj,
            "categories": categories,
            "selected_category": selected_category,
        },
    )


def communities(request):
    all_communities = Community.objects.order_by("name")
    return render(request, "posts/communities.html", {"communities": all_communities})


def community_detail(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    community_posts = community.posts.order_by("-created_at")
    return render(
        request,
        "posts/community_detail.html",
        {"community": community, "posts": community_posts},
    )


def search(request):
    query = request.GET.get("q", "").strip()
    posts = Post.objects.none()
    communities = Community.objects.none()
    events = Event.objects.none()

    if query:
        posts = Post.objects.filter(
            Q(content__icontains=query) | Q(author__username__icontains=query)
        ).order_by("-created_at")
        communities = Community.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).order_by("name")
        events = Event.objects.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(location__icontains=query)
        ).order_by("event_date")

    return render(
        request,
        "posts/search.html",
        {"query": query, "posts": posts, "communities": communities, "events": events},
    )


def lost_found(request):
    items = LostFoundItem.objects.order_by("status", "-created_at")
    return render(request, "posts/lost_found.html", {"items": items})


@login_required
def create_lost_found_item(request):
    if request.method == "POST":
        form = LostFoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.reporter = request.user
            item.save()
            return redirect("lost_found")
    else:
        form = LostFoundItemForm()

    return render(request, "posts/create_lost_found_item.html", {"form": form})


def profile(request, username):
    user_model = get_user_model()
    profile_user = get_object_or_404(user_model, username=username)
    student_profile, _ = Profile.objects.get_or_create(user=profile_user)
    user_posts = Post.objects.filter(author=profile_user).order_by("-created_at")
    return render(
        request,
        "posts/profile.html",
        {"profile_user": profile_user, "profile": student_profile, "posts": user_posts},
    )


@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user).order_by("-created_at")
    stats = {
        "posts": user_posts.count(),
        "likes_received": Like.objects.filter(post__author=request.user).count(),
        "comments_received": Comment.objects.filter(post__author=request.user).count(),
        "events_created": Event.objects.filter(created_by=request.user).count(),
        "rsvps": RSVP.objects.filter(user=request.user).count(),
        "items_reported": LostFoundItem.objects.filter(reporter=request.user).count(),
    }
    return render(
        request,
        "posts/dashboard.html",
        {"stats": stats, "recent_posts": user_posts[:5]},
    )


@login_required
def export_my_posts(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="campusconnect_posts.csv"'

    writer = csv.writer(response)
    writer.writerow(["Content", "Community", "AI Category", "Created At"])
    for post in Post.objects.filter(author=request.user).order_by("-created_at"):
        writer.writerow(
            [
                post.content,
                post.community.name if post.community else "",
                post.ai_category,
                post.created_at.strftime("%Y-%m-%d %H:%M"),
            ]
        )
    return response


@login_required
def edit_profile(request):
    student_profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=student_profile)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=student_profile)

    return render(request, "posts/edit_profile.html", {"form": form})


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.ai_category = predict_category(post.content)
            post.save()
            return redirect("home")
    else:
        form = PostForm()

    return render(request, "posts/create_post.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.ai_category = predict_category(updated_post.content)
            updated_post.save()
            return redirect("home")
    else:
        form = PostForm(instance=post)

    return render(request, "posts/edit_post.html", {"form": form, "post": post})


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(user=request.user, post=post)

    if like.exists():
        like.delete()
    else:
        Like.objects.create(user=request.user, post=post)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                message="liked your post.",
                post=post,
            )

    return redirect("home")


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    message="commented on your post.",
                    post=post,
                )
            return redirect("home")
    else:
        form = CommentForm()

    return render(
        request,
        "posts/add_comment.html",
        {"form": form, "post": post},
    )


@login_required
def report_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        return redirect("home")

    existing_report = Report.objects.filter(reporter=request.user, post=post).first()
    if existing_report:
        return redirect("home")

    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.post = post
            report.save()
            return redirect("home")
    else:
        form = ReportForm()

    return render(request, "posts/report_post.html", {"form": form, "post": post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        post.delete()

    return redirect("home")


@login_required
def toggle_bookmark(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    bookmark = Bookmark.objects.filter(user=request.user, post=post)
    if bookmark.exists():
        bookmark.delete()
    else:
        Bookmark.objects.create(user=request.user, post=post)
    return redirect("home")


@login_required
def saved_posts(request):
    saved = Bookmark.objects.filter(user=request.user).select_related(
        "post", "post__author", "post__community"
    ).order_by("-created_at")
    return render(request, "posts/saved_posts.html", {"saved": saved})


def events(request):
    all_events = Event.objects.order_by("event_date")
    return render(request, "posts/events.html", {"events": all_events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_going = False
    if request.user.is_authenticated:
        is_going = event.rsvps.filter(user=request.user).exists()
    return render(
        request,
        "posts/event_detail.html",
        {"event": event, "is_going": is_going},
    )


@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect("events")
    else:
        form = EventForm()

    return render(request, "posts/create_event.html", {"form": form})


@login_required
def toggle_rsvp(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    rsvp = RSVP.objects.filter(user=request.user, event=event)

    if rsvp.exists():
        rsvp.delete()
    else:
        RSVP.objects.create(user=request.user, event=event)
        if event.created_by != request.user:
            Notification.objects.create(
                recipient=event.created_by,
                actor=request.user,
                message="RSVP'd to your event.",
                event=event,
            )

    return redirect("events")


@login_required
def notifications(request):
    items = Notification.objects.filter(recipient=request.user).select_related(
        "actor", "post", "event"
    ).order_by("-created_at")
    items.filter(is_read=False).update(is_read=True)
    return render(request, "posts/notifications.html", {"notifications": items})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "posts/signup.html", {"form": form})
