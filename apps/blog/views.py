from typing import Any

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
)
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.decorators import action
from  rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)


from apps.blog.models import Post, Comment
from apps.blog.serializer import (
    PostBaseSerializer,
    PostListSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    CommentListSerializer,
    CommentCreateSerializer
)
from apps.blog.permissions import IsPostAuthor

class PostViewSet(GenericViewSet):
    
    queryset = Post.objects.all().filter(deleted_at__isnull=True)
    serializer_class = PostBaseSerializer
    lookup_field = 'slug'

    def list(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[Any,Any]) -> DRFResponse:
        queryset = self.get_queryset().filter(status=Post.STATUS_PUBLISHED).order_by('-created_at')
        serializer = PostListSerializer(queryset, many= True)
        return DRFResponse(serializer.data)
    
    def retrieve(self, request: DRFRequest, *args, **kwargs) -> DRFResponse:
        post = self.get_object()  
        serializer = PostListSerializer(post)
        return DRFResponse(serializer.data)

    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        serializer = PostCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )

        post = serializer.save(author=request.user)


        return DRFResponse(
            data=PostListSerializer(post).data,
            status=HTTP_201_CREATED
        )
    
    def get_permissions(self):
        if self.action in ['partial_update', 'destroy']:
            return [IsAuthenticatedOrReadOnly(), IsPostAuthor()]
        if self.action in ['create', 'comments']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]

    def partial_update(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> DRFResponse:
        """Update the User"""
        post = self.get_object()
        serializer = PostUpdateSerializer(post, data=request.data, partial=True)

        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status = HTTP_400_BAD_REQUEST
            )

        post = serializer.save()

        return DRFResponse(
                data=PostListSerializer(post).data,
                status=HTTP_200_OK
        )

    def destroy(self, request: DRFRequest, *args, **kwargs) -> DRFResponse:
        post = self.get_object()  
        post.delete()  # вызовет твой soft delete — поставит deleted_at
        return DRFResponse(status=HTTP_204_NO_CONTENT)
    
    @action(
        detail=True,
        methods=['GET', 'POST'],
        url_path='comments',
        permission_classes=[IsAuthenticatedOrReadOnly],
    )
    def comments(self, request: DRFRequest, slug: str = None) -> DRFResponse:
        post = self.get_object()

        if request.method == 'GET':
            comments = Comment.objects.filter(
                post=post,
                deleted_at__isnull=True
            ).order_by('-created_at')
            serializer = CommentListSerializer(comments, many=True)
            return DRFResponse(serializer.data)

        # POST
        serializer = CommentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return DRFResponse(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )

        serializer.save(author=request.user, post=post)
        return DRFResponse(serializer.data, status=HTTP_201_CREATED)