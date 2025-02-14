from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # Replace if using a remote DB
DB_NAME = "chatbot"

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]
chat_collection = database["chat_logs"]
