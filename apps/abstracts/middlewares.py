from typing import Callable, Optional, Any

from django.utils.translation import activate, deactivate
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.users.models import CustomUser
from settings.base import DEFAULT_LANGUAGE_CODE

def UserLanguageMiddleware(get_response: Callable) -> Callable:
    """User preferred language identificattion middleware"""
    
    def get_user_id_from_jwt(request: WSGIRequest) -> Optional[int]:
        """Exract user_id from JWT token"""

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        
        access_token:str = auth_header.strip().split(" ")[1]

        try:
            payload:dict[str, Any] = AccessToken(access_token)
            return payload.get("user_id")
        except TokenError:
            return None
        
        
    def determine_language(request:WSGIRequest) -> str:
        """Determines the language for that will be used in request"""

        user_id: Optional[int] = get_user_id_from_jwt(request)  
        if user_id is not None:
            return CustomUser.objects.get(pk=user_id).preferred_language
        
        query_lang: Optional[str] = request.GET.get('lang')
        if query_lang is not None: 
            return normalize(query_lang)
        
        header_lang: Optional[str] = request.headers.get("Accept-Language")
        if query_lang is not None:
            return normalize(header_lang)

        return DEFAULT_LANGUAGE_CODE 
    

    def normalize(lang:str) -> str:
        """Normalizing language code"""

        lang = lang.lower()
        return lang if lang in CustomUser.LANGUAGE_CODES else DEFAULT_LANGUAGE_CODE


    def middleware(request: WSGIRequest) -> DRFResponse:
        """Takes request language header and process"""
        lang = determine_language(request)
        activate(lang)
        print(lang)
        request.LANGUAGE_CODE = lang

        response: DRFResponse = get_response(request)
        response.headers.setdefault("Content-Language", lang)
            
        deactivate()

        return response
    
    return middleware