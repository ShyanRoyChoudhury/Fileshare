from rest_framework.response import Response
from rest_framework.decorators import api_view,  permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers.SignInSerializer  import SignInSerializer
from .serializers.FileListSerializer import FileListSerializer
from .serializers.SignUpSerializer import SignUpSerializer
from .serializers.FileDownloadSerializer import FileDownloadSerializer
from .serializers.FileDeleteSerializer import FileDeleteSerializer
from .serializers.GenerateFileLinkSerializer import GenerateFileLinkSerializer
from .serializers.VerifyMFASerializer import VerifyMFASerializer
from .encryption.encrypt import EncryptionHandler
from django.http import FileResponse
from django.core.files.base import ContentFile
import urllib.parse
import pyotp
import qrcode
import io
import base64

import os
from .models import Files, FileDownloadLink, User
import mimetypes
from datetime import timedelta
from django.utils import timezone

# Create your views here.

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
        print("inside api")
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
                        'status': "Success",
                        'user': result.get('user')
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
    

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def getList(request):
    try:
        print("test print")
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
        if not os.path.exists(filepath):
            return Response({
                'data': {
                    'status': "Fail",
                    'message': "File not found on server"
                },
            })
        
        with open(filepath, 'rb') as encrypted_file:
            encrypted_content = encrypted_file.read()
        
        decryption_handler = EncryptionHandler()
        try:
            decrypted_content = decryption_handler.decrypt_file(encrypted_content)

        except Exception as e:
            print("Decryption error:", e)
            return Response({
                'data': {
                    'message': "Error decrypting file"
                }
            })

        decrypted_file = ContentFile(decrypted_content)
        response = FileResponse(
            decrypted_file,
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

        response['Content-Length'] = len(decrypted_content)

        if 'X-Sendfile' in response:
            del response['X-Sendfile']
        return response
            
        
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
    

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def generateLink(request, uid):
    try:
        serializers = GenerateFileLinkSerializer(data={'uid':str(uid)})

        if not serializers.is_valid():
            return Response({
                'data': {
                    'status': "Fail",
                    'message': 'validation error'
                }
            })
        
        file = Files.objects.filter(uid=uid, deleted=False).first()
        if not file:
            return Response({
                'data': {
                    'status': "Fail",
                    'message': "File not found"
                }
            })

        expires_at = timezone.now() + timedelta(hours=24)
        temp_link = FileDownloadLink.objects.create(
            file=file,
            expires_at=expires_at
        )
        # Return the download link
        download_link = f"http://localhost:8000/api/downloadTemp/{temp_link.token}/"
        return Response({
            'status': "Success",
            'data': {
                'download_link': download_link,
                'expires_at': expires_at
            }
        })
    except Exception as e:
        print("ERROR", e)
        return Response({
            'data': {
                'status': "Fail",
                'message': "Internal server Error"
            }
        }, status=500)
    


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def downloadFileTempLink(request, token):
    try:
        # Get the temporary download link
        print("temp_link", token)
        temp_link = FileDownloadLink.objects.filter(token=str(token)).first()
        print("temp_link", temp_link)
        print("temp_link_test")
        if not temp_link:
            return Response({
                'status': "Fail",
                'message': "Invalid download link"
            }, status=404)

        # Check if the link has expired
        if temp_link.is_expired():
            return Response({
                'status': "Fail",
                'message': "Download link has expired"
            }, status=410)  # 410 Gone

        # Check if the link has already been used
        if temp_link.is_used:
            return Response({
                'status': "Fail",
                'message': "Download link has already been used"
            }, status=403)  # 403 Forbidden

        # Get the file
        file_obj = temp_link.file
        filepath = file_obj.file.path
        if not os.path.exists(filepath):
            return Response({
                'status': "Fail",
                'message': "File not found on server"
            }, status=404)

        # Serve the file
        response = FileResponse(
            open(filepath, 'rb'),
            as_attachment=True,
            filename=file_obj.name
        )
        mime_type, _ = mimetypes.guess_type(filepath)
        response['Content-Type'] = mime_type if mime_type else "application/octet-stream"
        safe_filename = urllib.parse.quote(file_obj.name)
        response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
        del response['X-Sendfile']

        # Mark the link as used
        temp_link.mark_as_used()

        return response
    except Exception as e:
        print("ERROR", e)
        return Response({
            'data': {
                'message': "Internal Server Error",
                'status': "Fail",
            }
        }, status=500)
    


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def Logout(request):
    response =  Response({
                'data': {
                    'status': "Success"
                }
            })

    response.set_cookie(
        key='access_token',  # Cookie name
        value='',
        httponly=True,  # Makes the cookie inaccessible to JavaScript
        secure=False,  # Only sends the cookie over HTTPS
        samesite='Lax',  # Provides CSRF protection
        max_age=0,  # Cookie expires in 24 hours
        path='/',  # Cookie is available for all paths
        domain='localhost'
    )

    return response


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def profile_view(request):
    try:
        userEmail = request.userEmail
        user_mfa = User.objects.filter(email=userEmail, deleted=False).first()
        if not user_mfa.mfa_secret:
            user_mfa.mfa_secret = pyotp.random_base32()
            user_mfa.save()
        
        otp_uri = pyotp.totp.TOTP(user_mfa.mfa_secret).provisioning_uri(
            name=user_mfa.email,
            issuer_name="Fileshare"
        )

        qr = qrcode.make(otp_uri)
        buffer = io.BytesIO()
        qr.save(buffer, format='PNG')

        buffer.seek(0)
        qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")
        qr_code_data_uri = f"data:image/png;base64,{qr_code}"
        return Response({
            "data": {
                'status': "Success",
                'qr_code': qr_code_data_uri,
                'email': user_mfa.email
            }
        })
    
    except Exception as e:
        print("ERROR", e)
        return Response({
            'data': {
                'message': "Internal Server Error",
                'status': "Fail",
            }
        }, status=200)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def verify_mfa(request):
    try:
        otp = request.data.get('otp')
        userEmail = request.userEmail

        serializer = VerifyMFASerializer(data={'otp': otp}, context={'userEmail': userEmail})

        if serializer.is_valid():
            success = serializer.verify_mfa()  # Now returns True/False
            if success:
                return Response({
                    "data": {
                        "status": "Success",
                        "message": "User 2FA enabled successfully"
                    }
                }, status=200)
            else:
                return Response({
                    "data": {
                        "status": "Fail",
                        "message": "Incorrect OTP"
                    }
                }, status=200)

        return Response({
            "data": {
                "status": "Fail",
                "message": "Invalid data"
            }
        }, status=200)

    except Exception as e:
        print("ERROR:", e)
        return Response({
            "data": {
                "message": "Internal Server Error",
                "status": "Fail"
            }
        }, status=200)