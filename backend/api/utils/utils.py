from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive an encryption key from a password and salt using PBKDF2.
    Equivalent to the JavaScript deriveKey function.
    """
    # Create PBKDF2HMAC instance with same parameters as JavaScript
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 bits = 32 bytes
        salt=salt,
        iterations=100000,  # Same as JavaScript
        backend=default_backend()
    )
    
    # Derive the key
    key = kdf.derive(password.encode('utf-8'))
    return key

def decrypt_file(encrypted_data, password):
    """
    Decrypt a file using the derived key.
    
    Args:
        encrypted_data (bytes): The encrypted file data
        password (str): The password used for key derivation
    
    Returns:
        bytes: The decrypted file content
    """
    try:
        # Extract IV, salt, and ciphertext just like in JavaScript
        iv = encrypted_data[:12]
        salt = encrypted_data[12:28]
        ciphertext = encrypted_data[28:]
        
        print("iv", iv)
        print("password", password)
        # Derive the key using the same process as JavaScript
        key = derive_key(password, salt)
        print("after derived key")
        # Create AESGCM cipher with derived key
        aesgcm = AESGCM(key)
        
        # Decrypt the data
        plaintext = aesgcm.decrypt(iv, ciphertext, None)
        return plaintext
        
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

