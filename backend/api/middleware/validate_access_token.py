import jwt
from django.conf import settings
from ..models import User
from django.http import JsonResponse
from django.urls import path

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
        excluded_paths = ["/api/signin", "/api/signUp", "/api/downloadTemp/", "/api/logout"]
        if any(request.path.startswith(path) for path in excluded_paths):
            return self.get_response(request)

        try:
            access_token = request.COOKIES.get('access_token')
            
            if access_token:
                # Add Authorization header
                request.META['HTTP_AUTHORIZATION'] = f"Bearer {access_token}"

                # Decode the token
                token = decode_token(access_token)

                if not isinstance(token, dict):  # Ensure token is decoded successfully
                    return JsonResponse({
                        'data': {
                            "status": "Fail",
                            "message": token
                        }
                    })
                
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
