from django.contrib import admin

from .models import Bookmark, Comment, Community, Event, Like, LostFoundItem, Notification, Post, Profile, Report, RSVP

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Community)
admin.site.register(Event)
admin.site.register(RSVP)
admin.site.register(Profile)
admin.site.register(Report)
admin.site.register(LostFoundItem)
admin.site.register(Notification)
admin.site.register(Bookmark)
