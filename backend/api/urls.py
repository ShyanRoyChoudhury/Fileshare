from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', hello_world), 
    path('upload/', post),
    path('signin', signIn),
    path('signUp', signUp),
    path('getList', getList)
]