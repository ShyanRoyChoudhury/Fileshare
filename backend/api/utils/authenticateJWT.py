from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
# from django.contrib.auth import get_user_model

# User = get_user_model()
from ..models import User

class EmailTimestampJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            email = validated_token.get("email")
            if not email:
                raise InvalidToken("Token missing email")
            print("email in email class", email)
            test = User.objects.get(email=email)    
            print("User in email calss", test)
        except User.DoesNotExist:
            raise InvalidToken("User not found")