from django.contrib.admin import (
    register,
    ModelAdmin
)
from apps.blog.models import Category, Tag, Post, Comment

@register(Post)
class PostAdmin(ModelAdmin):
    ...

@register(Category)
class PostAdmin(ModelAdmin):
    ...

@register(Tag)
class PostAdmin(ModelAdmin):
    ...

@register(Comment)
class PostAdmin(ModelAdmin):
    ... 