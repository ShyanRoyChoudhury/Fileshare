from rest_framework.response import Response
from rest_framework.decorators import api_view,  permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers.SignInSerializer  import SignInSerializer
from .serializers.FileListSerializer import FileListSerializer
from .serializers.SignUpSerializer import SignUpSerializer
from .serializers.FileDownloadSerializer import FileDownloadSerializer
from .serializers.FileDeleteSerializer import FileDeleteSerializer
from django.http import FileResponse
import urllib.parse

from .models import Files
import os
import mimetypes

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
        files = Files.objects.filter(user=user, deleted=False).values('uid', 'file', 'created_at', 'name')
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
            'data': {
                'status': "Fail",
                'data': None,
                'message': "Internal Server Error"
            }
        })
    

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def downloadFile(request, uid):
    try:
        userEmail = request.userEmail
        serializer = FileDownloadSerializer(data={'uid':str(uid)})
        if not serializer.is_valid():
            return Response({
                'status': 200,
                'message': 'validation error'
            })

        # filepath = Files.objects.filter(uid=str(uid)).values('file')
        file_obj = Files.objects.filter(uid=str(uid), deleted=False).first()
        if not file_obj:
            return Response({
                'data': {
                    'status': "Fail",
                    'message': "File not found"
                }
            })
        filepath = file_obj.file.path
        if os.path.exists(filepath):
            response = FileResponse(
            open(filepath, 'rb'),
            as_attachment=True,  # Force download
            filename=file_obj.name  # Original filename
            )
        
            # Add additional headers to force download
            mime_type, _ = mimetypes.guess_type(filepath)
            response['Content-Type'] = mime_type if mime_type else "application/octet-stream"
            # response['Content-Type'] = 'application/octet-stream'
            # response['Content-Disposition'] = f'attachment; filename="{file_obj.name}"'
            safe_filename = urllib.parse.quote(file_obj.name)
            response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
            del response['X-Sendfile']
            return response
            
        return Response({
                'data': {
                    'status': "Fail",
                    'message': "File not found on server"
                },
            })
    except Exception as e:
        print("ERRROR", e)
        return Response({
            'data': {
                'status': "Fail",
                'data': None,
                'message': "Internal Server Error"
            }
        })
    
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def deleteFile(request, uid):
    try:
        serializer = FileDeleteSerializer(data={'uid': str(uid)})
        if not serializer.is_valid():
            return Response({
                'data': {
                    'status': "Fail",
                    'data': None,
                    'message': 'validation error'
                }
            })
        # delete_file = Files.objects.update_or_create(uid=uid, defaults={'deleted': True})
        # if not delete_file:
        #     return Response({
        #         'data': {
        #             'status': "Fail",
        #             'data': None,
        #             'message': 'File delete operation failed'
        #         }
        #     })
        

        # return Response({
        #         'data': {
        #             'status': "Success",
        #             'data': None,
        #             'message': 'File deleted'
        #         }
        #     })

        try:
            file_obj = Files.objects.get(uid=str(uid))
        except Files.DoesNotExist:
            return Response({
                'data': {
                    'status': "Fail",
                    'data': None,
                    'message': "File not found"
                }
            }, status=404)

        # Delete file from file system
        file_path = file_obj.file.path  
        if file_path and os.path.exists(file_path):
            os.remove(file_path)  # Delete file from storage

        # Delete record from database
        file_obj.delete()

        return Response({
            'data': {
                'status': "Success",
                'data': None,
                'message': "File deleted successfully"
            }
        })
    except Exception as e:
        print("ERRROR", e)
        return Response({
            'data': {
                'status': "Fail",
                'data': None,
                'message': "Internal Server Error"
            }
        })