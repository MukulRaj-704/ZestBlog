from django.urls import path
from .views import (
    BlogListView, BlogDetailView,
    BlogCreateView, BlogUpdateView, BlogDeleteView,
    toggle_like, follow_toggle,
    inbox, start_conversation, delete_message,
    share_blog, get_mutual_friends, send_file,
    following_feed
)

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('follow/<str:username>/', follow_toggle, name='follow_toggle'),
    path('feed/', following_feed, name='following_feed'),  # ← add this
    path('inbox/', inbox, name='inbox'),
    path('inbox/<int:conversation_id>/', inbox, name='conversation_detail'),
    path('inbox/<int:conversation_id>/send-file/', send_file, name='send_file'),
    path('message/<str:username>/', start_conversation, name='start_conversation'),
    path('message/delete/<int:message_id>/', delete_message, name='delete_message'),
    path('api/friends/', get_mutual_friends, name='get_mutual_friends'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<slug:slug>/edit/', BlogUpdateView.as_view(), name='blog_update'),
    path('<slug:slug>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('<slug:slug>/like/', toggle_like, name='blog_like'),
    path('<slug:slug>/share/', share_blog, name='share_blog'),
]