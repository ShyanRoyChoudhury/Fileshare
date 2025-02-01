from cryptography.fernet import Fernet
from django.conf import settings
from django.core.files.base import ContentFile

# key = Fernet.generate_key()
 
# # string the key in a file
# with open('filekey.key', 'wb') as filekey:
#    filekey.write(key)


# class encryptFile():
#     def __init__(self, key):
#        self.fernet = Fernet(key)

#    # opening the original file to encrypt
#     def encrypt(self, filepath):
#         with open(filepath, 'rb') as file:
#             original = file.read()

#         encrypted = self.fernet.encrypt(original)

#         # opening the file in write mode and 
#         # writing the encrypted data
#         with open(filepath, 'wb') as encrypted_file:
#             encrypted_file.write(encrypted)

#         return encrypted
      
#     def decrypt(self, filepath):
#         # using the key
#         fernet = Fernet(key)
 
#         # opening the encrypted file
#         with open(filepath, 'rb') as enc_file:
#             encrypted = enc_file.read()
 
#         # decrypting the file
#         decrypted = fernet.decrypt(encrypted)
        
#         # opening the file in write mode and
#         # writing the decrypted data
#         with open(filepath, 'wb') as dec_file:
#             dec_file.write(decrypted)

#         return decrypted




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