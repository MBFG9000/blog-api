from django.urls import path

from apps.blog.views import PostAPIView

urlpatterns = [
    path('post', view=PostAPIView.as_view())
]