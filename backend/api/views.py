from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *

# Create your views here.

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, React!"})


@api_view(['POST'])
def post(request):
    try:

        data = request.FILES.getlist('files')
        print("DATA", data)
        serializer = FileListSerializer(data={"files": data})

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'message': 'files uploaded successfully'
            })
        
        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors
        })
    except Exception as e:
        print("ERRROR", e)
        return Response({
            'status': 500,
            'message': 'Internal server error',
        })