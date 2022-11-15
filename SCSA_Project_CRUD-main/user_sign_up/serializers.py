from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()

MIN_LENGTH = 1
PASSWORD_MIN_LENGTH = 8
EMAIL_MIN_LENGTH = 9
MAX_LENGTH = 120


class UserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH,
        required=True,
        error_messages={
            "min_length": f"name must be longer than {MIN_LENGTH} characters.",
            "max_length": f"name must be shorter than {MAX_LENGTH} characters.",
            "required": "This field must be filled in.",
        }
    )

    last_name = serializers.CharField(
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH,
        required=True,
        error_messages={
            "min_length": f"lastname must be longer than {MIN_LENGTH} characters.",
            "max_length": f"lastname must be shorter than {MAX_LENGTH} characters.",
            "required": "This field must be filled in.",
        }
    )

    email = serializers.EmailField(
        min_length=EMAIL_MIN_LENGTH,
        required=True,
        error_messages={
            "min_length": f"email must be longer than {EMAIL_MIN_LENGTH} characters.",
            "required": "This field must be filled in.",
        }
    )

    password1 = serializers.CharField(
        write_only=True,
        required=True,
        min_length=PASSWORD_MIN_LENGTH,
        style={'input_type': 'password', 'placeholder': 'Password'},
        error_messages={
            "required": "This field must be filled in.",
            "min_length": f"password must be longer than {PASSWORD_MIN_LENGTH} characters.",
        }
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        min_length=PASSWORD_MIN_LENGTH,
        style={'input_type': 'password', 'placeholder': 'Password'},
        error_messages={
            "required": "This field must be filled in.",
            "min_length": f"password must be longer than {PASSWORD_MIN_LENGTH} characters.",

        }
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

    def validate(self, data):
        print('---------------serializer--------------------------------')
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords don't match!")

        return super().validate(data)

    def create(self, validated_data):
        print('-----------------------------------------------')
        user = User.objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password1"])
        user.save()

        return user
