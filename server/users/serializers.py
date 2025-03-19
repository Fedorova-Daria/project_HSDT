from rest_framework import serializers
from .models import Account
from django.contrib.auth.hashers import make_password
from core.models import UniversityGroup


class AccountSerializer(serializers.ModelSerializer):
    university_group = serializers.PrimaryKeyRelatedField(queryset=UniversityGroup.objects.all(), required=False)
    class Meta:
        model = Account
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'company_name',
                  'university_group', 'role', 'phone', 'bio', 'skills', 'avatar', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        if "username" not in validated_data:
            validated_data["username"] = validated_data["email"]  # Если нет username, ставим email

        # Хешируем пароль перед сохранением
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)

        # Создаем пользователя
        return super().create(validated_data)


