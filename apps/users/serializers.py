from zoneinfo import available_timezones

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    ValidationError
)

from apps.users.models import CustomUser

class CustomUserRegisterSerializer(ModelSerializer):    
    password = CharField(write_only=True)
    password_confirm = CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'avatar',
            'password',
            'password_confirm',
        ]
        read_only_fields = [
            'id',
            'is_active',
        ]
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise ValidationError({"password" : "passwords do not match"})
        return attrs
    
    def create(self, validate_data):
        """Create new user with encrypted password"""
        
        validate_data.pop("password_confirm")
        password = validate_data.pop("password")

        user = CustomUser(**validate_data)
        user.set_password(password)
        user.save()
        
        return user

class CustomUserLocalizationSerializer(ModelSerializer):
    """
    Serializer that used in RetrieveUpdateView for requesting and patching 
    localization info
    """
    class Meta:
        """
        Serializer meta class
        """
        model = CustomUser
        fields = [
            'preferred_language',
            'timezone'
        ]

    def validate_timezone(self, value :str) -> str:
        """Validates timezone value"""
        if value not in available_timezones():
            raise ValidationError(f"Invalid timezone: {value}")
        
        return value
    