from django import forms
from .models import Blog, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'cover_image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-700 bg-white dark:bg-gray-800 '
                         'text-gray-900 dark:text-white focus:outline-none '
                         'focus:ring-2 focus:ring-primary',
                'placeholder': 'Enter blog title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-700 bg-white dark:bg-gray-800 '
                         'text-gray-900 dark:text-white focus:outline-none '
                         'focus:ring-2 focus:ring-primary',
                'placeholder': 'enter-slug-like-this'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-700 bg-white dark:bg-gray-800 '
                         'text-gray-900 dark:text-white focus:outline-none '
                         'focus:ring-2 focus:ring-primary',
                'rows': 8,
                'placeholder': 'Write your blog content here...'
            }),
            'cover_image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-700 bg-white dark:bg-gray-800 '
                         'text-gray-900 dark:text-white'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-primary'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 '
                         'dark:border-gray-700 bg-white dark:bg-gray-800 '
                         'text-gray-900 dark:text-white focus:outline-none '
                         'focus:ring-2 focus:ring-primary',
                'rows': 3,
                'placeholder': 'Write your comment...'
            }),
        }