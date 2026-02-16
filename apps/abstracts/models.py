# Python models
from typing import Any

# Django models
from django.db.models import Model, DateTimeField
from django.utils import timezone as django_timezone

class AbstractBaseModel(Model):
    """
    Abstract base model with fields that common for all models
    """

    created_at = DateTimeField(
        auto_now_add=True
    )
    updated_at = DateTimeField(
        auto_now=True
    )
    deleted_at = DateTimeField(
        null=True
    )

    class Meta:
        """Meta class for AbstractBaseModel."""

        abstract = True

    def delete(self, *args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> None:
        """Soft delete the object by setting deleted_at timestamp."""

        self.deleted_at = django_timezone.now()
        self.save(update_fields=["deleted_at"])

