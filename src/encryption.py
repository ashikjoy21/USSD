import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import datetime

# Function to create a short hash from the input data
def create_short_hash(data):
    hasher = hashlib.sha256(data.encode())
    short_hash = hasher.hexdigest()[:16]  # Truncate the hash to 16 characters
    return short_hash

# Function to encrypt data using AES with a dynamic key and a fixed IV
def encrypt_data(acc_no, message, timestamp=None, key=b'supersecretkey123', iv=b'fixedinitializ'):
    # Derive a secure key from the provided key
    dynamic_key = hashlib.sha256(key).digest()
    iv = iv[:16].ljust(16, b'\0')  # Ensure IV is 16 bytes long

    # Use current timestamp if not provided
    if not timestamp:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Combine acc_no, timestamp, and message
    combined_data = f"{acc_no}|{timestamp}|{message}"

    # Initialize AES cipher with the dynamic key and fixed IV
    cipher = AES.new(dynamic_key, AES.MODE_CBC, iv)
    padded_data = pad(combined_data.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)

    # Encode the encrypted data and truncate if necessary
    encrypted_code = base64.b64encode(encrypted_data).decode('utf-8')
    return encrypted_code[:16]  # Shortened for demonstration

# Example usage
acc_no = "1234567890"
message = "Transaction details"
timestamp = "2024-11-07 12:34:56"  # Example timestamp
encrypted_code = encrypt_data(acc_no, message, timestamp)

print("Encrypted Code:", encrypted_code)
