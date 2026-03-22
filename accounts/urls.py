from . import views
from django.urls import path 
from .views import (
    UserProfileView, EditProfileView,
    CustomPasswordChangeDoneView, CustomPasswordChangeView
)
from .views import UserProfileView, EditProfileView, CustomPasswordChangeDoneView,CustomPasswordChangeView
urlpatterns=[
    path('register/',views.RegisterView, name ='register'),
    path('login/', views.loginView, name= 'login'),
    path('logout/',views.logoutView, name='logout'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

]