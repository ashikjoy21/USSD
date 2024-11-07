from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import secrets
import uuid

app = FastAPI()

class TransactionData(BaseModel):
    acc_no: str
    message: str
    bank_id: str  # New field for bank ID
    timestamp: str = None

# Dictionary to store keys (for demonstration purposes)
key_storage = {}

# Function to generate a new encryption key
def generate_key():
    return secrets.token_bytes(16)  # Generate a random 16-byte (128-bit) key

# Function to store the generated key
def store_key():
    today = datetime.date.today()
    key_storage[today] = generate_key()  # Store the key with today's date

# Function to retrieve the key for today
def get_key_for_today():
    today = datetime.date.today()
    return key_storage.get(today)

# Initialize key storage at startup
store_key()

# AES encryption function with a daily key
def encrypt_data(data: str) -> str:
    key = get_key_for_today()  # Retrieve today's key
    if key is None:
        raise Exception("No key found for today")

    fixed_iv = b'1234567890123456'  # Fixed IV (for demonstration purposes)
    
    cipher = AES.new(key, AES.MODE_CBC, fixed_iv)
    padded_data = pad(data.encode(), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.urlsafe_b64encode(encrypted).decode()

@app.post("/generate-simple-code/")
async def generate_simple_code(data: TransactionData):
    # Use the current time as the timestamp if not provided
    if not data.timestamp:
        data.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Use a fixed UUID for demonstration
    fixed_mid = "123e4567-e89b-12d3-a456-426614174000"  # Example of a fixed UUID

    # Concatenate the data
    combined_data = f"{data.acc_no}|{data.timestamp}|{data.message}|{data.bank_id}"
    
    # Encrypt the combined data
    encoded_code = encrypt_data(combined_data)

    return {"mid": fixed_mid, "bank_id": data.bank_id, "encoded_code": encoded_code}

# To run the app, use:
# uvicorn your_script_name:app --reload
