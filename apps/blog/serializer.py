from typing import Any, Optional
from datetime import datetime
from zoneinfo import ZoneInfo

from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    StringRelatedField,
    ValidationError,
    CharField,
    ListField,
    ChoiceField
)
from rest_framework.request import Request as DRFRequest
from babel.dates import format_datetime

from apps.blog.models import (
    Post,
    Category, 
    Tag, 
    Comment,
    CategoryTranslations
)
from apps.abstracts.serializers import CustomUserForeignSerializer

class PostBaseSerializer(ModelSerializer):
    """
    Base serilizer for Post instances
    """

    class Meta:
        """
        Serializer meta data
        """
        model = Post
        fields = "__all__"

class CategorySerializer(Serializer):
    name = SerializerMethodField()
    slug = CharField()
    
    def get_name(self,obj: Category) -> str:
        language = get_language()
        translation = obj.translations.filter(language=language).first()
        
        if translation:
            return translation.name
        
        return obj.name

class PostListSerializer(PostBaseSerializer):

    author = CustomUserForeignSerializer()
    status = SerializerMethodField()
    tags = StringRelatedField(many=True, read_only = True)
    category = CategorySerializer()
    created_at = SerializerMethodField()
    updated_at = SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id',
            'slug',
            'category',
            'tags',
            'author',
            'title',
            'body',
            'status',
            'author',
            'created_at',
            'updated_at'
        ]

    def get_status(self, obj) -> str:
        return obj.get_status_display()
    
    def format_local_datetime(self, dt:datetime, request:Optional[DRFRequest] = None):
        lang = get_language() 
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            tz_str = request.user.timezone 
        else:
            tz_str = 'UTC'
        
        tz = ZoneInfo(tz_str)
        localized = dt.astimezone(tz)
        
        return format_datetime(localized, format='long', locale=lang)

    def get_created_at(self, obj):
        request = self.context.get('request')
        return self.format_local_datetime(obj.created_at, request)
    
    def get_updated_at(self, obj):
        request = self.context.get('request')
        return self.format_local_datetime(obj.updated_at, request)


class PostCreateSerializer(PostBaseSerializer):
    """
    Serializer for Post instances
    """
    category = CharField(required=False, allow_null=True, allow_blank=True)
    tags = ListField(
        child=CharField(),
        required=False,
        default=list
    )
    status = ChoiceField(
    choices=[(label, label) for label in Post.TEXT_CHOICES.values()],
    default=Post.STATUS_DRAFT_LABEL,
    required=False,
    )


    class Meta:
        model = Post
        fields = (
            'title',
            'body',
            'category',
            'tags',
            'status'
        )

    def validate_category(self, value:str) -> Category|None:
        """Validates is category is existing"""
        if not value:
            return None
        category = Category.objects.filter(name=value).first()
        if not category:
            raise ValidationError(f"Category '{value}' does not exist")
        return category
    
    def validate_tags(self, value: list[str]) -> list[Tag]:
        if not value:
            return []
        tags = []
        for tag_name in value:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        return tags
    
    def create(self, validated_data: dict[Any, Any]) -> Post:
        tags = validated_data.pop('tags', [])
        category = validated_data.pop('category', None)

        post = Post.objects.create(**validated_data, category=category)

        if tags:
            post.tags.set(tags)

        return post 

    def validate_status(self, value: str) -> str:
        for code, label in Post.TEXT_CHOICES.items():
            if label == value:
                return code
        raise ValidationError(f"Invalid status '{value}'.")
    
class PostUpdateSerializer(PostBaseSerializer):
    category = CharField(required=False, allow_null=True, allow_blank=True)
    tags = ListField(
        child=CharField(),
        required=False,
        default=None
    )
    status = ChoiceField(
        choices=[(label,label) for label in Post.TEXT_CHOICES.values()],
        default = Post.STATUS_DRAFT_LABEL,
        required=False
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'category',
            'tags',
            'status',
        ]

    def validate_category(self, value:str) -> Category|None:
        if not value:
            return None
        
        category = Category.objects.filter(name=value).first()

        if not category:
            raise ValidationError(_(f"Category '{value}' does not exist.") % {value})
        
        return category
    
    def validate_tags(self, value: list[str]) -> list[Tag]:
        if value is None:
            return None

        tags = []

        for tag_name in value:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        return tags
    
    def validate_status(self, value: list[str]) -> list[Tag]:
        for code, label in Post.TEXT_CHOICES.items():
            if label == value:
                return code
            
        raise ValidationError(f"Invalid status '{value}'.")

    def update(self, instance: Post, validated_data:dict[str,str]) -> Post:
        tags = validated_data.pop('tags', None)
        category = validated_data.pop('category', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if category is not None:
            instance.category = category

        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        return instance
    

class CommentBaseSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentListSerializer(CommentBaseSerializer):
    author = CharField(source='author.email', read_only=True)
    post = CharField(source='post.slug', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'post',
            'body',
            'created_at',
        ]

class CommentCreateSerializer(CommentBaseSerializer):
    class Meta:
        model = Comment
        fields = [
            'body'
        ]

