import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

def create_short_hash(data):
    hasher = hashlib.sha256(data.encode())
    short_hash = hasher.hexdigest()[:16]
    return short_hash

def encrypt_data(data, key=b'supersecretkey123', iv=b'initializationVe'):
    dynamic_key = hashlib.sha256(key).digest()
    iv = iv[:16].ljust(16, b'\0')

    cipher = AES.new(dynamic_key, AES.MODE_CBC, iv)
    padded_data = pad(data.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    encrypted_code = base64.b64encode(encrypted_data).decode('utf-8')[:16]
    return encrypted_code
