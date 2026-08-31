from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Event, LostFoundItem, Post, Profile, Report


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["community", "content", "image"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "What would you like to share?",
                }
            )
            ,
            "image": forms.ClearableFileInput(
                attrs={"accept": "image/*"}
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Write a comment...",
                }
            )
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "community", "event_date", "location", "description"]
        widgets = {
            "event_date": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
            "description": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Tell students about the event..."}
            ),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["department", "year", "bio"]
        widgets = {
            "bio": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Tell the campus about yourself..."}
            ),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reason", "details"]
        widgets = {
            "details": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Optional: explain what happened..."}
            ),
        }


class LostFoundItemForm(forms.ModelForm):
    class Meta:
        model = LostFoundItem
        fields = ["item_type", "title", "description", "location", "image"]
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Describe the item clearly..."}
            ),
            "image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
