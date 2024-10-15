import uvicorn
from src.api import app  # Import the FastAPI app from src/api.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        app,  # Pass the imported app instance here
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", 8000)),
        reload=bool(os.getenv("DEBUG", True))
    )
