from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    EmailField,
)

from restaccounts.models import ExtendedUser


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = ExtendedUser
        fields = [
            # 'username',
            'name',
        ]


class RegisterSerializer(ModelSerializer):
    email = EmailField(label='Email adress')

    class Meta:
        model = ExtendedUser
        fields = [
            'id',
            'username',
            'password',
            'email',
        ]

    extra_kwargs = {"password":
                        {"write_only": True},
                    "id":
                        {"read_only": True}
                    }

    def validate(self, data):
        return data

    def validate_email(self, value):
        email = value
        user_qs = ExtendedUser.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("Email alredy registred")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user_obj = ExtendedUser(
            username=username,
            email=email,
        )
        user_obj.set_password(password)
        user_obj.save()
        return user_obj


class UserEditSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = ExtendedUser
        fields = [
            'id',
            # 'username',
            'password',
            'email',
        ]

    extra_kwargs = {"password":
                        {"write_only": True},
                    "id":
                        {"read_only": True}
                    }

    def update(self, validated_data, instance):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.email = validated_data.get('email')

        instance.save()
        return instance()


class ProfileEditSerializer(ModelSerializer):
    class Meta:
        model = ExtendedUser
        fields = [
            'username',
            'id',
            'name',
            'tel',
            'image',
            'first_name',
            'last_name'
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"read_only": True}
        }
