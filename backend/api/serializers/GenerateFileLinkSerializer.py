from rest_framework import serializers

class GenerateFileLinkSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=50, allow_blank=False)