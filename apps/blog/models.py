# Python modules
from typing import Any

# Django modules
from django.db import models
from django.db.models import (
    CharField,
    SlugField,
    ForeignKey,
    TextField,
    ManyToManyField,
    DateTimeField,
    CASCADE,
    SET_NULL,
)
from django.utils.text import slugify

# Project modules
from apps.abstracts.models import AbstractBaseModel
from apps.users.models import CustomUser

class Category(AbstractBaseModel):
    """
    Category model represents category of blog 
    """

    NAME_MAX_LEN = 100

    name = CharField(max_length=NAME_MAX_LEN, unique=True)
    slug = SlugField(unique=True, blank=True)

    def __str__(self) -> str:
        """Returns the string representation of the category"""
        return self.name
    
    def __repr__(self) -> str:
        """Returns the official string representation of the object."""
        return f"Category(id={self.id}, name={self.name}, slug={self.slug})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Tag(AbstractBaseModel):
    """
    Tag model represents tags that associated  with post
    """

    NAME_MAX_LEN = 50

    name = CharField(max_length=NAME_MAX_LEN, unique=True)
    slug = SlugField(unique=True, blank=True)

    def __str__(self) -> str:
        """Returns the string representation of the Tag"""
        return self.name
    
    def __repr__(self) -> str:
        """Returns the official string representation of the object."""
        return f"Category(id={self.id}, name={self.name}, slug={self.slug})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Tag.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
class Post(AbstractBaseModel):  
    """
    Post object that store the posts of authors
    """

    TITLE_MAX_LEN = 200
    STATUS_DRAFT = "drft"
    STATUS_DRAFT_LABEL = "draft"
    STATUS_PUBLISHED = "pub"
    STATUS_PUBLISHED_LABEL = "published"
    TEXT_CHOICES = {
        STATUS_DRAFT: STATUS_DRAFT_LABEL,
        STATUS_PUBLISHED: STATUS_PUBLISHED_LABEL,
    }

    author = ForeignKey(to=CustomUser, on_delete=CASCADE)
    title = CharField(max_length=TITLE_MAX_LEN)
    slug = SlugField(unique=True, blank=True)
    body = TextField()
    category = ForeignKey(to=Category, 
    null=True, 
    blank=True, 
    on_delete=SET_NULL,
    )
    tags = ManyToManyField(Tag, blank=True)
    status = CharField(choices=TEXT_CHOICES)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Returns the string representation of the Tag"""
        return self.title



class Comment(AbstractBaseModel):
    post = ForeignKey(Post, on_delete=CASCADE)
    author = ForeignKey(to=CustomUser, on_delete=CASCADE)
    body = TextField()     

