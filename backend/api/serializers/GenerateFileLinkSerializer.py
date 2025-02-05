# serializers.py
from rest_framework import serializers
from ..models import PermissionTypes

class GenerateFileLinkSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=100, allow_blank=False)
    permission = serializers.ChoiceField(choices=['Read', 'Write'])

    def validate_permission(self, value):
        """ 
            Convert string permission to enum value
        """
        try:
            print('PermissionTypes[value].value', PermissionTypes[value].value)
            return PermissionTypes[value].value
        except KeyError:
            print('inside KeyError')
            return PermissionTypes.Read.value
    