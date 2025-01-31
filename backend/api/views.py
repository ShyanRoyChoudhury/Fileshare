from rest_framework.response import Response
from rest_framework.decorators import api_view,  permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers.SignInSerializer  import SignInSerializer
from .serializers.FileListSerializer import FileListSerializer
from .serializers.SignUpSerializer import SignUpSerializer
from .models import Files
# Create your views here.

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, React!"})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny]) 
def post(request):
    try:
        data = request.FILES.getlist('files')
        print("DATA", data)
        # user = request.COOKIES.get('access_token')
        user = request.userEmail
        print("user from view", user)
        
        # file_data = [{"file": file} for file in files]
        serializer = FileListSerializer(data={"files": data}, context={'user': user})

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'message': 'files uploaded successfully'
            })
        
        return Response({
            'status': 400,
            'message': 'Something went wrong',
        })
    except Exception as e:
        print("ERRROR", e)
        return Response({
            'status': 500,
            'message': 'Internal server error',
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def signIn(request):
    try:
        # Check if request.data exists and is not empty
        if not request.data:
            return Response({
                'status': 200,
                'data': {
                    'message': "Validation Failed",
                    'status': "Fail"
                }
            })

        # Safely get idToken with get() method to avoid KeyError
        data = request.data.get('idToken')
        
        # Check if idToken is None or empty
        if not data:
            return Response({
                'status': 200,
                # 'message': 'Sign in unsuccessful',
                'data': {
                    'message': "IdToken is required",
                    'status': "Fail"
                }
            })
        serializer = SignInSerializer(data={'idToken': data})

        if serializer.is_valid():
            result = serializer.signin()
            print("result", result)
            if result is None:  # Using 'is None' for explicit None check
                return Response({
                    'status': 200,
                    # 'message': 'Sign-in Failed',
                    'data': {
                        'requireRegistration': True,
                        'status': "Success"
                    }
                })
                
            response =  Response({
                # 'message': 'Sign in Successful',  # Fixed typo
                'data': {
                    'requireRegistration': False,
                    'user': result.get("user"),
                    'status': "Success"
                }
            })

            response.set_cookie(
                key='access_token',  # Cookie name
                value=result.get("accessToken"),
                httponly=True,  # Makes the cookie inaccessible to JavaScript
                secure=False,  # Only sends the cookie over HTTPS
                samesite='Lax',  # Provides CSRF protection
                max_age=3600 * 24,  # Cookie expires in 24 hours
                path='/',  # Cookie is available for all paths
                domain='localhost'
            )
            # response['Access-Control-Allow-Origin'] = 'http://localhost:5173'
            response['Access-Control-Allow-Credentials'] = 'true'
            return response
        else:
            # Handle invalid serializer data
            return Response({
                'status': 200,
                # 'message': 'Sign in unsuccessful',
                'data': {
                    'message': serializer.errors,
                    'success': "Fail"
                }
            })
            
    except Exception as e:
        print("Error", e)
        return Response({
            'status': 200,
            'data': {
                    'message': 'Internal server error',
                    'status': "Fail"
                }  
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def signUp(request):
    try:
        idToken = request.data.get('idToken')
        email = request.data.get('email')

        serializer = SignUpSerializer(data={'idToken': idToken})
        if serializer.is_valid():
            result = serializer.signUp()
            if result.get("created") is False:
                return Response({
                    'status': 200,
                    'data': {
                            'message': 'User Registration Failed',
                            'status': "Fail"
                        }  
                    })    
            return Response({
            'status': 200,
            'data': {
                    'message': 'User Registered',
                    'status': "Success"
                }  
            })
        

    except Exception as e:
        print("Error", e)
        return Response({
            'status': 200,
            'data': {
                    'message': 'Internal server error',
                    'status': "Fail"
                }  
        })
    

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def getList(request):
    try:
        user = request.userEmail
        # files = Files.objects.get(user=user)
        files = Files.objects.filter(user=user).values('uid', 'file', 'created_at', 'name')
        print('files', files)
        return Response({
            'status': 200,
            'data': {
                'status': "Success",
                'data': list(files)
            },
        })
            
    except Exception as e:
        print("ERRROR", e)
        return Response({
            'status': 500,
            'message': 'Internal server error',
        })