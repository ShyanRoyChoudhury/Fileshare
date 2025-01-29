from django.urls import path
from .views import hello_world, post

urlpatterns = [
    path('hello/', hello_world), 
    path('upload/', post)
]