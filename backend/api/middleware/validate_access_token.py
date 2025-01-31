import jwt
from django.conf import settings
from ..models import User

def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"


class AccessTokenMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_paths = ["/api/signin", "/api/signUp"]
        if request.path in excluded_paths:
            return self.get_response(request)

        try:
            access_token = request.COOKIES.get('access_token')
            print("access_token", access_token)
            
            if access_token:
                # Add Authorization header
                request.META['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"

                # Decode the token
                token = decode_token(access_token)
                print("Decoded token:", token)

                if isinstance(token, dict):  # Ensure token is decoded successfully
                    email = token.get('email')
                    if email:
                        # Query the User model
                        try:
                            user = User.objects.get(email=email, deleted=False)
                            print("User found:", user)
                            request.userEmail = user
                        except User.DoesNotExist:
                            print("User not found or deleted.")
                    else:
                        print("Invalid token structure.")
            return self.get_response(request)  # Ensure this is returned

        except Exception as e:
            print("Error:", e)
            return self.get_response(request)  # Ensure this is returned
