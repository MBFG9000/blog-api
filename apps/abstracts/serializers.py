from rest_framework.serializers import ModelSerializer

from apps.users.models import CustomUser

class CustomUserForeignSerializer(ModelSerializer):
    """
    Serializer for CustomUser foreign key representation.
    """

    class Meta:
        """
        Customize the serializer's metadata.
        """

        model = CustomUser
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'avatar'
        )