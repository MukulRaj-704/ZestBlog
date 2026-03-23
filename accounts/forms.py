from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": (
                    "w-full px-4 py-3 rounded-lg "
                    "bg-gray-50 dark:bg-gray-800 "
                    "border border-gray-300 dark:border-gray-700 "
                    "text-gray-900 dark:text-white "
                    "placeholder-gray-400 "
                    "focus:ring-2 focus:ring-primary focus:outline-none"
                )
            })


class EditProfileExtrasForm(forms.ModelForm):
    """Handles only bio — avatar handled by Cloudinary widget"""
    class Meta:
        model = UserProfile
        fields = ['bio']  # ✅ removed 'avatar'
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-gray-800 '
                         'border border-gray-300 dark:border-gray-700 '
                         'text-gray-900 dark:text-white '
                         'focus:ring-2 focus:ring-primary focus:outline-none',
                'rows': 3,
                'placeholder': 'Write something about yourself...'
            }),
        }