from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from django.urls import path

from apps.users.views import (
    CreateUserAPIView,
    RetrieveUpdateUser
)

urlpatterns = [
    path('auth/register', CreateUserAPIView.as_view()),
    path('auth/token', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('auth/localization', RetrieveUpdateUser.as_view(), name="user_localization")
]

