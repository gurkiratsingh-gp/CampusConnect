from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Community, Event, Like, Notification, Post, RSVP


class CampusConnectTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="testpass123")
        self.student = User.objects.create_user(username="student", password="testpass123")
        self.community = Community.objects.create(
            name="BSc Computer Science",
            description="Computer science student community.",
        )
        self.post = Post.objects.create(
            author=self.owner,
            community=self.community,
            content="Welcome to CampusConnect!",
        )
        self.event = Event.objects.create(
            title="Python Workshop",
            description="Learn Python together.",
            event_date=timezone.now() + timedelta(days=7),
            location="Computer Lab 2",
            community=self.community,
            created_by=self.owner,
        )

    def test_public_pages_load(self):
        for url in [
            reverse("home"),
            reverse("communities"),
            reverse("events"),
            reverse("event_detail", args=[self.event.id]),
            reverse("lost_found"),
        ]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_create_post_requires_login(self):
        response = self.client.get(reverse("create_post"))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_student_can_create_post(self):
        self.client.force_login(self.student)
        response = self.client.post(
            reverse("create_post"),
            {"community": self.community.id, "content": "Hello from a new student!"},
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(
            Post.objects.filter(author=self.student, content="Hello from a new student!").exists()
        )

    def test_like_creates_notification_for_post_owner(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse("toggle_like", args=[self.post.id]))
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(Like.objects.filter(user=self.student, post=self.post).exists())
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.owner,
                actor=self.student,
                post=self.post,
            ).exists()
        )

    def test_rsvp_creates_notification_for_event_creator(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse("toggle_rsvp", args=[self.event.id]))
        self.assertRedirects(response, reverse("events"))
        self.assertTrue(RSVP.objects.filter(user=self.student, event=self.event).exists())
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.owner,
                actor=self.student,
                event=self.event,
            ).exists()
        )

    def test_student_cannot_edit_another_students_post(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("edit_post", args=[self.post.id]))
        self.assertEqual(response.status_code, 404)

    def test_student_can_export_own_posts(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("export_my_posts"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response["Content-Type"])
        self.assertIn(b"Welcome to CampusConnect!", response.content)
