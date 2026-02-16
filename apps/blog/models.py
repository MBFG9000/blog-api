# Python modules


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

# Project modules
from apps.abstracts.models import AbstractBaseModel
from apps.auths.models import CustomUser

class Category(AbstractBaseModel):
    """
    Category model represents category of blog 
    """

    NAME_MAX_LEN = 100

    name = CharField(max_length=NAME_MAX_LEN, unique=True)
    slug = SlugField(unique=True)

    def __str__(self) -> str:
        """Returns the string representation of the category"""
        return self.name
    
    def __repr__(self) -> str:
        """Returns the official string representation of the object."""
        return f"Category(id={self.id}, name={self.name}, slug={self.slug})"


class Tag(AbstractBaseModel):
    """
    Tag model represents tags that associated  with post
    """

    NAME_MAX_LEN = 50

    name = CharField(max_length=NAME_MAX_LEN, unique=True)
    slug = SlugField(unique=True)

    def __str__(self) -> str:
        """Returns the string representation of the Tag"""
        return self.name
    
    def __repr__(self) -> str:
        """Returns the official string representation of the object."""
        return f"Category(id={self.id}, name={self.name}, slug={self.slug})"
    

class Post(AbstractBaseModel):  
    """
    Post object that store the posts of authors
    """

    TITLE_MAX_LEN = 200
    STATUS_DRAFT = 1
    STATUS_DRAFT_LABEL = "draft"
    STATUS_PUBLISHED = 2
    STATUS_PUBLISHED_LABEL = "published"
    TEXT_CHOICES = {
        STATUS_DRAFT: STATUS_DRAFT_LABEL,
        STATUS_PUBLISHED: STATUS_PUBLISHED_LABEL,
    }

    author = ForeignKey(to=CustomUser, on_delete=CASCADE)
    title = CharField(max_length=TITLE_MAX_LEN)
    slug = SlugField(unique=True)
    body = TextField
    category = ForeignKey(to=Category, 
    null=True, 
    blank=True, 
    on_delete=SET_NULL,
    )
    tags = ManyToManyField(Tag, blank=True)
    status = CharField(choices=TEXT_CHOICES)


class Comment(AbstractBaseModel):
    post = ForeignKey(Post, on_delete=CASCADE)
    author = ForeignKey(to=CustomUser, on_delete=CASCADE)
    body = TextField     

