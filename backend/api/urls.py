from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', post),
    path('signin', signIn),
    path('signUp', signUp),
    path('logout', Logout),
    path('getList', getList),
    path('download/<uuid:uid>/', downloadFile, name='download_file'),
    path('delete/<uuid:uid>/', deleteFile, name='delete_file'),
    path('generateLink/<uuid:uid>/', generateLink, name='generate_file_link'),
    path('downloadTemp/<str:token>/', downloadFileTempLink, name='download_link_file'),
    path('profile', profile_view, name='profile_view'),
    path('mfaOtpVerify', verify_mfa, name='otp_verify'),  
    path('serveFiles/<str:token>/', serve_encrypted_file, name='serve_files'),   
]