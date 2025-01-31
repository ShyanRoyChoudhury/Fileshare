
from rest_framework import serializers
from ..models import *
from .SignInSerializer import validate_user
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import get_user_model



# User = get_user_model()
class SignUpSerializer(serializers.Serializer):
    """
        validates the email and idToken and creates a new User
    """
    idToken = serializers.CharField(allow_blank=False)

    def signUp(self):
        idToken = self.validated_data['idToken']
        print(" inside signup serializer")
        validated_user = validate_user(idToken)
        print("user:", validated_user)

        email = validated_user.get('email')
        print("email", email)
        user, created = User.objects.get_or_create(email=email, defaults={"email": validated_user.get('email', '')})
        print(f"user {user} \n created {created}")
        return {
            "user": {
                "email": user.email,
                # "name": user.name,
                "created": created,  # True if a new user was created, False if user already existed
            },
        }