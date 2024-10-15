from fastapi import FastAPI
from pydantic import BaseModel
from .encryption import encrypt_data
from .ai_context import extract_message_context
from .model import CustomGPTModel
import datetime

app = FastAPI()

# Load your custom GPT model
gpt_model = CustomGPTModel("models/custom_gpt_model")

class TransactionData(BaseModel):
    transaction_amount: str
    acc_no: str
    message: str
    timestamp: str = None

def prepare_data_for_encryption(transaction_amount, acc_no, timestamp, context):
    return f"{transaction_amount}{acc_no}{timestamp}{context}"

@app.post("/generate-encrypted-code/")
async def generate_encrypted_code(data: TransactionData):
    if not data.timestamp:
        data.timestamp = datetime.datetime.now().isoformat()

    context = extract_message_context(data.message)
    combined_data = prepare_data_for_encryption(data.transaction_amount, data.acc_no, data.timestamp, context)
    encrypted_code = encrypt_data(combined_data)

    return {"encrypted_code": encrypted_code}
