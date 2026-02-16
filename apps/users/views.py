from typing import Any
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import HTTP_201_CREATED

from apps.users.models import CustomUser
from apps.users.serializers import CustomUserRegisterSerializer

class CreateUserAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def get_tokens_for_user(user:CustomUser) -> object:
        """Returns JWT tokens for special user""" 

        refresh = RefreshToken.for_user(user)
        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }

    def create(self, request: DRFRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]):
        """Creates new CustomUser and return credential with token"""
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = self.get_tokens_for_user(user)
        return DRFResponse(
            {**serializer.data, **tokens}, status=HTTP_201_CREATED
        )



