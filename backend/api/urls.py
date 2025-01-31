from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', hello_world), 
    path('upload/', post),
    path('signin', signIn),
    path('signUp', signUp),
    path('getList', getList),
    path('download/<uuid:uid>/', downloadFile, name='download_file'),
    path('delete/<uuid:uid>/', deleteFile, name='delete_file'),
]