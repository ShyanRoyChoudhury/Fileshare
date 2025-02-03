from cryptography.fernet import Fernet
from django.conf import settings
from django.core.files.base import ContentFile


class EncryptionHandler:
    def __init__(self):
        # Store key in Django settings or environment variable instead of file
        self.key = getattr(settings, 'AES_ENCRYPTION_KEY', Fernet.generate_key())
        self.fernet = Fernet(self.key)
        print("self.key", self.key)
    def encrypt_file(self, file_data):
        file_content = file_data.read()
        encrypted_data = self.fernet.encrypt(file_content)
        
        # Create a ContentFile with a name
        encrypted_file = ContentFile(encrypted_data)
        # Set the name attribute required by FileField
        encrypted_file.name = file_data.name
        
        return encrypted_file

    def decrypt_file(self, encrypted_data):
        # Decrypt the file data
        return self.fernet.decrypt(encrypted_data)