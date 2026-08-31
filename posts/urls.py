from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('notifications/', views.notifications, name='notifications'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export-posts/', views.export_my_posts, name='export_my_posts'),
    path('lost-found/', views.lost_found, name='lost_found'),
    path('lost-found/create/', views.create_lost_found_item, name='create_lost_found_item'),
    path('communities/', views.communities, name='communities'),
    path('communities/<int:community_id>/', views.community_detail, name='community_detail'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('create-post/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('posts/<int:post_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('saved-posts/', views.saved_posts, name='saved_posts'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/report/', views.report_post, name='report_post'),
    path('signup/', views.signup, name='signup'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('events/', views.events, name='events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/rsvp/', views.toggle_rsvp, name='toggle_rsvp'),
]
