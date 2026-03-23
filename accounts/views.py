from django.shortcuts import render, redirect 
from . models import User
from django.contrib.auth import login, logout, authenticate
from . forms import RegisterForm 
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from blog.models import Blog
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import EditProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.views import View


User = get_user_model()

# Create your views here.

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('blog_list')
    else:
        form = RegisterForm()
    return render(request,'accounts/register.html', {'form' : form})

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request,user)
            return redirect('blog_list')
        else:
            return render(request, 'accounts/login.html', {'error': "Invalid Credentials"})
    return render(request, 'accounts/login.html')


def logoutView(request):
    logout(request)
    return redirect('login')


from accounts.models import UserProfile

class UserProfileView(ListView):
    model = Blog
    template_name = 'accounts/profile.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        self.profile_user = User.objects.get(username=self.kwargs['username'])
        return Blog.objects.filter(
            author=self.profile_user,
            is_published=True
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, _ = UserProfile.objects.get_or_create(user=self.profile_user)
        context['profile_user'] = self.profile_user
        context['profile'] = profile
        context['total_blogs'] = self.get_queryset().count()
        context['is_following'] = False
        if self.request.user.is_authenticated and self.request.user != self.profile_user:
            try:
                my_profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
                context['is_following'] = profile in my_profile.follows.all()
            except Exception:
                pass
        return context

from .forms import RegisterForm, EditProfileForm, EditProfileExtrasForm

class EditProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/edit_profile.html'

    def get(self, request):
        user_form = EditProfileForm(instance=request.user)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile_form = EditProfileExtrasForm(instance=profile)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    def post(self, request):
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile_form = EditProfileExtrasForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_instance = profile_form.save(commit=False)

            # ✅ Save Cloudinary URL directly
            avatar_url = request.POST.get('avatar_url')
            if avatar_url:
                profile_instance.avatar = avatar_url
        
            profile_instance.save()
            return redirect('user_profile', username=request.user.username)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('password_change_done')


from django.contrib.auth.views import PasswordChangeDoneView

class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'accounts/change_password_done.html'
