# Python modules
from typing import Any

# Django modules
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
    DateTimeField,
    ImageField,
)
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password



# Project modules
from apps.abstracts.models import AbstractBaseModel
from apps.users.validators import validate_email_domain


class CustomUserManager(BaseUserManager):
    """Custom User Manager to make database requests"""
    
    def __obtain_user_intance(
        self,
        email: str,
        first_name: str,
        last_name:str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Get user intance."""

        if not email:
            raise ValidationError(
                message="Email field is required", 
                code="email_empty"  
            )
        if not first_name:
            raise ValidationError(
                message="first_name is required",
                code="first_name_empty",
            )
        if not last_name:
            raise ValidationError(
                message="last_name is required",
                code="last_name_empty",
            )
        
        new_user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs
        )

        return new_user
    
    def create_user(
        self,
        email: str,
        first_name: str,
        last_name:str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Create custom user"""
        new_user: 'CustomUser' = self.__obtain_user_intance(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user
    
    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name:str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'CustomUser':
        """Create super user. Used by manage.py createsuperuser."""
        new_user: 'CustomUser' = self.__obtain_user_intance(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user
    

class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """
    Custom User extending AbstactUserModel
    """
    EMAIL_MAX_LENGTH = 150
    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50
    PASSWORD_MAX_LENGTH = 254

    email = EmailField(
        max_length=EMAIL_MAX_LENGTH,
        validators=[validate_email_domain,],
        unique=True,
        db_index=True,
        verbose_name="Email address",
        help_text="User's email address",
    )
    first_name = CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name="First name",
        help_text="User's first name",
    )
    last_name = CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        null=False,
        blank=False,
        verbose_name="Last name",
        help_text="User's last name",
    )
    is_active = BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
    )
    is_staff = BooleanField(
        default=False,
        verbose_name="Staff status",
        help_text="Designates whether the user can log into this admin site."
    )
    date_joined = DateTimeField(
        auto_now_add=True
    )
    avatar = ImageField(
        null=True,
        blank=True,
    )
    password = CharField(
        max_length=PASSWORD_MAX_LENGTH,
        validators=[validate_password],
        verbose_name="Password",
        help_text="User's hash representation of the password"
    )

    REQUIRED_FIELDS = ["first_name", "last_name"]
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        """Meta options for CustomUser model."""

        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ["-created_at"]


    

