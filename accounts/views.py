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
        context['profile_user'] = self.profile_user
        context['total_blogs'] = self.get_queryset().count()
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'user_profile',
            kwargs={'username': self.request.user.username}
        )



class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('password_change_done')


from django.contrib.auth.views import PasswordChangeDoneView

class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'accounts/change_password_done.html'
