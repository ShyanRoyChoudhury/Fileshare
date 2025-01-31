from rest_framework import serializers

class FileDeleteSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=50, allow_blank=False)