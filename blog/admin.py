from django.contrib import admin
from .models import Blog , Comment
# Register your models he00re.

@admin.register(Blog)
class blogadmin(admin.ModelAdmin):
    list_display = ('title','author','is_published','created_at')
    list_filter= ('is_published','created_at')
    search_fields = ('title','content')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Comment)