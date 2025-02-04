from rest_framework import serializers
from ..models import PermissionTypes

class DownloadFileTempLinkSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64, allow_blank=False)
    permission = serializers.CharField(max_length=10, allow_blank=False)
    
    def validate_permission(self, value):
    # Convert string permission to enum value
        try:
            return PermissionTypes[value].value
        except KeyError:
            return PermissionTypes.Read.value