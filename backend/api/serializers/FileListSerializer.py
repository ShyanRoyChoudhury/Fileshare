from rest_framework import serializers
from ..models import *


class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length = 10000, allow_empty_file = False, use_url = False)
    )

    def create(self, validated_date):
        user = self.context.get('user')
        print("user from serializer", user.email)
        try:
            db_user = User.objects.get(email=user.email)
            print("Database user:", db_user)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist in the database.")
        files = validated_date.pop('files')
        files_objs = []
        for file in files:
            print("file", file)
            files_obj = Files.objects.create(file = file, user=db_user, name = file.name)
            files_objs.append(files_obj)

        return files_objs  
