from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    bio = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    content = models.TextField(max_length=500)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    ai_category = models.CharField(max_length=30, default="General")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]


class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=150)
    community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="rsvps",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")


class Report(models.Model):
    class Reason(models.TextChoices):
        SPAM = "spam", "Spam or misleading"
        HARASSMENT = "harassment", "Harassment or bullying"
        INAPPROPRIATE = "inappropriate", "Inappropriate content"
        OTHER = "other", "Other"

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports")
    reason = models.CharField(max_length=20, choices=Reason.choices)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    class Meta:
        unique_together = ("reporter", "post")


class LostFoundItem(models.Model):
    class ItemType(models.TextChoices):
        LOST = "lost", "Lost item"
        FOUND = "found", "Found item"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        RESOLVED = "resolved", "Resolved"

    item_type = models.CharField(max_length=10, choices=ItemType.choices)
    title = models.CharField(max_length=150)
    description = models.TextField()
    location = models.CharField(max_length=150)
    image = models.ImageField(upload_to="lost_found/", blank=True, null=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications",
    )
    message = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor.username} {self.message}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
