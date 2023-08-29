from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя по модели RUD"""
    class Meta:
        model = User
        fields = ('id', 'username', 'tg_user_id', 'first_name', 'last_name', 'is_active',)


class UserCreateSerializer(serializers.Serializer):
    """Сериализатор создания пользователя"""
    username = serializers.CharField(max_length=150)
    description = serializers.SerializerMethodField(read_only=True)

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            is_active=False
        )
        user.save()