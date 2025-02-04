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
from .serializers.DownloadFileTempLinkSerializer import DownloadFileTempLinkSerializer
from .encryption.encrypt import EncryptionHandler
from django.http import FileResponse
from django.core.files.base import ContentFile
from django.http import HttpResponse
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
        # salt = request.POST.get('salt')  # Assuming salt is sent as base64
        # iv = request.POST.get('iv') 
        key = request.POST.get('key') 
        print("DATA", data)
        # user = request.COOKIES.get('access_token')
        user = request.userEmail
        print("user from view", user)
        
        # file_data = [{"file": file} for file in files]
        serializer = FileListSerializer(data={"files": data, "key": key}, context={'user': user})

        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': {
                    'message': 'files uploaded successfully',
                    'status': "Success"
                }
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
    

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def generateLink(request, uid):
    try:
        permission = request.GET.get('permission')
        serializers = GenerateFileLinkSerializer(data={'uid':str(uid), 'permission': permission})

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
        validated_permission = serializers.validate_permission('permission')
        print("validated_permission", validated_permission)
        temp_link = FileDownloadLink.objects.create(
            file=file,
            expires_at=expires_at,
            permission=validated_permission
        )
        # Return the download link
        download_link = f"http://localhost:8000/api/serveFiles/{temp_link.token}?permission={permission}#key={file.key}"
        return Response({
            'status': "Success",
            'data': {
                'download_link': download_link,
                'expires_at': expires_at,
                'permission': permission
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
        permission = request.GET.get('permission')

        serializers = DownloadFileTempLinkSerializer(data={'token': token, 'permission': permission})
        if not serializers.is_valid():
            return Response({
                'status': "Fail",
                'message': 'validation error'
            })

        temp_link = FileDownloadLink.objects.filter(token=str(token)).first()
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
            }, status=410)

        # Check if the link has already been used
        if temp_link.is_used:
            return Response({
                'status': "Fail",
                'message': "Download link has already been used"
            }, status=403)

        file_obj = temp_link.file
        filepath = file_obj.file.path

        if not os.path.exists(filepath):
            return Response({
                'status': "Fail",
                'message': "File not found on server"
            }, status=404)

        # Read the entire file content first
        with open(filepath, 'rb') as file:
            file_content = file.read()

        # If you have encryption, handle it here similar to the working API
        decryption_handler = EncryptionHandler()
        try:
            file_content = decryption_handler.decrypt_file(file_content)
        except Exception as e:
            print("Decryption error:", e)
            return Response({
                'status': "Fail",
                'message': "Error decrypting file"
            })

        # Create a ContentFile from the content
        content_file = ContentFile(file_content)

        # Create response with the content file
        response = FileResponse(
            content_file,
            as_attachment=True,
            filename=file_obj.name
        )

        # Set the proper headers
        mime_type, _ = mimetypes.guess_type(filepath)
        response['Content-Type'] = mime_type if mime_type else "application/octet-stream"
        
        safe_filename = urllib.parse.quote(file_obj.name)
        response['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
        
        response['Content-Length'] = len(file_content)

        if 'X-Sendfile' in response:
            del response['X-Sendfile']

        # Mark the link as used before sending
        temp_link.mark_as_used()
        print("temp_link.permission == 2", temp_link.permission)
        if temp_link.permission == 1:
            try:
                print("inside delete")
                # First ensure the file handle is closed
                content_file.close()
                
                # Delete the file from filesystem
                if os.path.exists(filepath):
                    os.remove(filepath)
                    
                # Optionally, update the file_obj to mark it as deleted in the database
                file_obj.deleted = True  # Assuming you have a deleted field
                file_obj.save()
                
                print(f"File deleted successfully: {filepath}")
            except Exception as e:
                print(f"Error deleting file: {e}")

        return response

    except Exception as e:
        print("ERROR:", e)
        return Response({
            'status': "Fail",
            'message': "Internal Server Error"
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
                'email': user_mfa.email,
                'name': user_mfa.name,
                'isMFAEnabled': user_mfa.mfa_enabled
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
    

# from django.http import HttpResponse
# import base64
# from django.shortcuts import get_object_or_404

# @api_view(['GET'])
# @authentication_classes([])
# @permission_classes([AllowAny])
# def serve_encrypted_file(request, token):
#     permission = request.GET.get('permission')
    
#     serializers = DownloadFileTempLinkSerializer(data={'token': token, 'permission': permission})
#     if not serializers.is_valid():
#         return HttpResponse("Validation error", status=400)

#     temp_link = get_object_or_404(FileDownloadLink, token=str(token))

#     if temp_link.is_expired():
#         return HttpResponse("Download link has expired", status=410)

#     if temp_link.is_used:
#         return HttpResponse("Download link has already been used", status=403)

#     file_obj = temp_link.file
#     file_path = file_obj.file.path

#     if not os.path.exists(file_path):
#         return HttpResponse("File not found on server", status=404)

#     with open(file_path, "rb") as file:
#         encrypted_data = file.read()

#     encryption_handler = EncryptionHandler()

#     try:
#         decrypted_cbc_data = encryption_handler.decrypt_file(encrypted_data)  # AES-CBC Decryption
#     except Exception as e:
#         return HttpResponse("Error decrypting file", status=500)

#     # Convert the remaining AES-GCM encrypted data to Base64 for transmission
#     encrypted_gcm_b64 = base64.b64encode(decrypted_cbc_data).decode()

#     # HTML + JS to decrypt AES-GCM in the browser
#     html_content = f"""
# <html>
# <head>
#     <title>Download File</title>
# </head>
# <body>
#     <h2>Decrypting and Downloading File...</h2>
#     <script>
#         async function decryptAndDownload() {{
#             // Extract the key from the URL fragment
#             const fragment = window.location.hash.substring(1); // Remove the '#' from the fragment
#             const params = new URLSearchParams(fragment); // Parse the fragment as URLSearchParams
#             const keyString = params.get("key"); // Get the key from the fragment

#             if (!keyString) {{
#                 document.body.innerHTML = "<h2>Missing decryption key!</h2>";
#                 return;
#             }}

#             // URL-decode the key before decoding Base64
#             const decodedKeyString = decodeURIComponent(keyString);
#             const keyBuffer = Uint8Array.from(atob(decodedKeyString), c => c.charCodeAt(0));

#             const key = await crypto.subtle.importKey(
#                 "raw", keyBuffer, { name: "AES-GCM" }, false, ["decrypt"]
#             );


#             // Convert Base64 file data to Uint8Array
#             const encryptedData = Uint8Array.from(atob("{encrypted_gcm_b64}"), c => c.charCodeAt(0));

#             try {{
#                 const iv = encryptedData.slice(0, 12);  // Extract IV
#                 const cipherText = encryptedData.slice(12);

#                 const decryptedBuffer = await crypto.subtle.decrypt(
#                     {{ name: "AES-GCM", iv }},
#                     key,
#                     cipherText
#                 );

#                 // Create a Blob from the decrypted data
#                 const blob = new Blob([decryptedBuffer], {{ type: "application/octet-stream" }});
#                 const link = document.createElement("a");
#                 link.href = URL.createObjectURL(blob);
#                 link.download = "{file_obj.name}"; // Set the filename for the download
#                 document.body.appendChild(link);
#                 link.click(); // Trigger the download
#                 link.remove(); // Clean up the DOM
#             }} catch (error) {{
#                 console.error("Decryption failed:", error);
#                 document.body.innerHTML = "<h2>Error decrypting file!</h2>";
#             }}
#         }}

#         // Automatically start the decryption and download process
#         decryptAndDownload();
#     </script>
# </body>
# </html>
# """

#     return HttpResponse(html_content, content_type="text/html")


from django.shortcuts import get_object_or_404

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def serve_encrypted_file(request, token):
    permission = request.GET.get('permission')

    # Validate the token and permission
    serializer = DownloadFileTempLinkSerializer(data={'token': token, 'permission': permission})
    if not serializer.is_valid():
        return HttpResponse("Validation error", status=400)

    # Fetch the temporary download link
    temp_link = get_object_or_404(FileDownloadLink, token=str(token))

    # Check if the link is expired or already used
    if temp_link.is_expired():
        return HttpResponse("Download link has expired", status=410)
    if temp_link.is_used:
        return HttpResponse("Download link has already been used", status=403)

    # Get the file object and its path
    file_obj = temp_link.file
    file_path = file_obj.file.path

    # Check if the file exists
    if not os.path.exists(file_path):
        return HttpResponse("File not found on server", status=404)

    # Read the encrypted file
    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    # Encode the encrypted data in Base64 for transmission
    encrypted_gcm_b64 = base64.b64encode(encrypted_data).decode()

    # Render the HTML template with the encrypted data
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Secure File Download</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .container {{
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            .status {{
                margin: 20px 0;
                font-size: 18px;
            }}
            .status.success {{
                color: green;
            }}
            .status.error {{
                color: red;
            }}
            .debug-info {{
                font-family: monospace;
                background-color: #f8f8f8;
                padding: 10px;
                border-radius: 4px;
                margin-top: 20px;
                max-height: 200px;
                overflow-y: auto;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Secure File Download</h2>
            <div id="status" class="status">Initializing secure download...</div>
            <div id="debugInfo" class="debug-info"></div>
        </div>

        <script>
            function arrayBufferToHex(buffer) {{
                return Array.from(new Uint8Array(buffer))
                    .map(b => b.toString(16).padStart(2, '0'))
                    .join('');
            }}

            function addDebugInfo(message) {{
                const debugDiv = document.getElementById('debugInfo');
                debugDiv.textContent += message + '\\n';
            }}

            async function decryptAndDownload() {{
                const statusDiv = document.getElementById('status');
                
                try {{
                    // Get key from URL fragment
                    const fragment = window.location.hash.substring(1);
                    const params = new URLSearchParams(fragment);
                    const keyString = params.get("key");

                    if (!keyString) {{
                        throw new Error("Missing decryption key in URL");
                    }}

                    addDebugInfo("Decoding key string...");
                    const decodedKeyString = decodeURIComponent(keyString);
                    const jwkKey = JSON.parse(decodedKeyString);
                    
                    addDebugInfo("JWK Key format:");
                    addDebugInfo(JSON.stringify(jwkKey, null, 2));

                    // Import the key
                    addDebugInfo("\\nImporting key...");
                    const key = await crypto.subtle.importKey(
                        "jwk",
                        jwkKey,
                        {{ name: "AES-GCM" }},
                        false,
                        ["decrypt"]
                    );
                    
                    addDebugInfo("\\nProcessing encrypted data...");
                    const base64Data = "{encrypted_gcm_b64}";
                    addDebugInfo(`Base64 data length: ${{base64Data.length}}`);
                    
                    const encryptedData = Uint8Array.from(atob(base64Data), c => c.charCodeAt(0));
                    addDebugInfo(`Encrypted data length: ${{encryptedData.length}}`);

                    // Extract components
                    const iv = encryptedData.slice(0, 12);
                    const salt = encryptedData.slice(12, 28);
                    const combinedData = encryptedData.slice(28);
                    const authTag = combinedData.slice(-16);  // Last 16 bytes are auth tag
                    const ciphertext = combinedData.slice(0, -16);  // Everything else is ciphertext
                    
                    addDebugInfo(`\\nIV length: ${{iv.length}}`);
                    addDebugInfo(`IV (hex): ${{arrayBufferToHex(iv)}}`);
                    addDebugInfo(`Salt length: ${{salt.length}}`);
                    addDebugInfo(`Salt (hex): ${{arrayBufferToHex(salt)}}`);
                    addDebugInfo(`Auth tag length: ${{authTag.length}}`);
                    addDebugInfo(`Auth tag (hex): ${{arrayBufferToHex(authTag)}}`);
                    addDebugInfo(`Ciphertext length: ${{ciphertext.length}}`);

                    // Combine ciphertext and auth tag for decryption
                    const finalCiphertext = new Uint8Array(ciphertext.length + authTag.length);
                    finalCiphertext.set(new Uint8Array(ciphertext), 0);
                    finalCiphertext.set(new Uint8Array(authTag), ciphertext.length);
                    
                    addDebugInfo("\\nAttempting decryption...");
                    const decryptedBuffer = await crypto.subtle.decrypt(
                        {{ 
                            name: "AES-GCM",
                            iv: new Uint8Array(iv),
                            tagLength: 128
                        }},
                        key,
                        finalCiphertext
                    );

                    addDebugInfo(`\\nDecryption successful! Decrypted size: ${{decryptedBuffer.byteLength}} bytes`);

                    const blob = new Blob([decryptedBuffer], {{ type: "application/octet-stream" }});
                    const link = document.createElement("a");
                    link.href = URL.createObjectURL(blob);
                    link.download = "{file_obj.name}";
                    
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                    URL.revokeObjectURL(link.href);
                    
                    statusDiv.textContent = "Download complete! You can close this window.";
                    statusDiv.className = "status success";

                }} catch (error) {{
                    console.error("Decryption failed:", error);
                    statusDiv.textContent = `Error: ${{error.name}} - ${{error.message}}`;
                    statusDiv.className = "status error";
                    addDebugInfo(`\\nERROR: ${{error.name}} - ${{error.message}}`);
                }}
            }}

            window.onload = decryptAndDownload;
        </script>
    </body>
    </html>
    """

    return HttpResponse(html_content, content_type="text/html")