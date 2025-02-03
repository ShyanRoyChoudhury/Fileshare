from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from ..models import *
from ..config import firebase_admin
from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
# import logger
from ..utils.RefreshToken import EmailTimestampRefreshToken

def validate_user(idToken):
    """
    Validates the Firebase ID token.

    Args:
        idToken (str): The Firebase ID token to validate.

    Returns:
        dict: The decoded token containing user information.

    Raises:
        ValueError: If the token is invalid or expired.
        FirebaseError: If there is an issue with the Firebase authentication.
    """
    try:
        # Use auth directly instead of firebase_admin.auth
        decoded_token = auth.verify_id_token(idToken)
        return decoded_token
    
    except ValueError as e:
        raise ValueError("Invalid or expired token.") from e
    
    except FirebaseError as e:
        raise FirebaseError(f"Firebase authentication error: {e}") from e
  

class SignInSerializer(serializers.Serializer):
    idToken = serializers.CharField(allow_blank=False)
    def signin(self): 
        """
        Validates the Firebase ID token and performs the sign-in logic.

        Returns:
            dict: A dictionary containing the result of the sign-in process.

        Raises:
            ValueError: If the token is invalid or expired.
            FirebaseError: If there is an issue with Firebase authentication.
        """
        try:
            idToken = self.validated_data['idToken']
            validated_user = validate_user(idToken)

            email = validated_user.get('email')
            if not email:
                # logger.error("No email found in Firebase token")
                raise ValueError("Email not found in Firebase token")

            try:
                user = User.objects.get(email=email, deleted=False)
                # logger.info(f"User found: {email}")
                print(f"User found: {email}")
            except User.DoesNotExist:
                return {"user": None}
            
            except Exception as e:
                # logger.error(f"Database error while fetching user: {str(e)}")
                raise AuthenticationFailed("Error accessing user data")
            # Generate JWT token
            refresh = EmailTimestampRefreshToken.for_user(user)
            print("refresh", refresh)
            return {
                "accessToken": str(refresh.access_token),
                "refreshToken": str(refresh),
                "user": {
                    "email": email,
                    "name": user.name,
                    "mfaEnabled": user.mfa_enabled
                },
            }

        except Exception as e:
            print("Error signing in:", e)
