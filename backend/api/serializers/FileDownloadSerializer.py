from rest_framework import serializers

class FileDownloadSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=50, allow_blank=False)