from rest_framework import serializers
from ..models import *
from ..encryption.encrypt import EncryptionHandler
from django.core.files.base import ContentFile
import base64

class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child = serializers.FileField(max_length = 10000, allow_empty_file = False, use_url = False)
    )
    # salt = serializers.CharField()
    # iv = serializers.CharField()
    key = serializers.CharField()


    # def validate_salt(self, value):
    #     try:
    #         salt = base64.b64decode(value)
    #         if len(salt) != 16:
    #             raise serializers.ValidationError("Invalid salt length")
    #         return value
    #     except Exception:
    #         raise serializers.ValidationError("Invalid salt encoding")

    # def validate_iv(self, value):
    #     try:
    #         iv = base64.b64decode(value)
    #         if len(iv) != 12:33
    #             raise serializers.ValidationError("Invalid IV length")
    #         return value
    #     except Exception:
    #         raise serializers.ValidationError("Invalid IV encoding")

    def create(self, validated_date):
        user = self.context.get('user')
        key = validated_date.get('key')
        print("user from serializer", user.email)
        try:
            db_user = User.objects.get(email=user.email)
            print("Database user:", db_user)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        
        encryption_handler = EncryptionHandler()
        files = validated_date.pop('files')
        files_objs = []
        for file in files:
            file_copy = ContentFile(file.read())
            file.seek(0)

            encrypted_file = encryption_handler.encrypt_file(file)
            print("Encrypted file type:", type(encrypted_file))
            print("Encrypted file content:", encrypted_file)

            print("encrypted_file", encrypted_file)
            files_obj = Files.objects.create(file = encrypted_file, user=db_user, name = file.name, deleted = False, key= key)
            files_objs.append(files_obj)
        return files_objs