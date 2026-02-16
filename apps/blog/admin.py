from django.contrib.admin import (
    register,
    ModelAdmin
)
from apps.blog.models import Category, Tag, Post, Comment

@register(Post)
class PostAdmin(ModelAdmin):
    ...
