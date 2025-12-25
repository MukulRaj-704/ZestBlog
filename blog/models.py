from django.db import models
from django.conf import settings 

# Create your models here.
user = settings.AUTH_USER_MODEL

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name='blogs')
    likes = models.ManyToManyField(user, related_name='liked_blogs', blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        user,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author}"