from django import forms
from .models import Comment,Blog

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': (
                        'w-full bg-white text-slate-900 '
                        'border border-slate-300 rounded-xl '
                        'p-4 focus:outline-none '
                        'focus:ring-2 focus:ring-blue-500 '
                        'min-h-[120px]'
                    ),
                    'placeholder': 'Write your comment here...',
                }
            )
        }
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "slug", "cover_image", "content", "is_published"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-slate-300 px-4 py-2 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            "slug": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-slate-300 px-4 py-2 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
            }),
            "cover_image": forms.ClearableFileInput(attrs={
                "class": "w-full text-slate-700"
            }),
            "content": forms.Textarea(attrs={
            "class": "w-full rounded-lg border border-slate-300 px-4 py-10 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y",
            "rows": 10,
            })
        }
