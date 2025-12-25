from django.urls import path
from .views import (
    BlogListView, BlogDetailView,
    BlogCreateView, BlogUpdateView, BlogDeleteView, toggle_like
)

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<slug:slug>/edit/', BlogUpdateView.as_view(), name='blog_update'),
    path('<slug:slug>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
     path('<slug:slug>/like/', toggle_like, name='blog_like'),
    
]
