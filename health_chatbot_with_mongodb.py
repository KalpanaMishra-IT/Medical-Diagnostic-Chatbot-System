from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
MONGODB_URI = os.getenv("mongodb+srv://ichikawakumiko0:8DCvkJISQ0CEb5ZM@cluster0.tywec.mongodb.net/")

# MongoDB Connection
try:
    client = MongoClient(MONGODB_URI)
    db = client["health_chatbot_db"]
    user_collection = db["user_data"]
    chat_collection = db["chat_logs"]
    print("✅ Connected to MongoDB!")
except Exception as e:
    print("❌ MongoDB Connection Error:", e)

# FastAPI App
app = FastAPI()

# Data Models
class HealthData(BaseModel):
    username: str
    activity_level: str
    miles_ran: int
    sleep_hours: float
    calories: int

class ChatInput(BaseModel):
    query: str

# Home Route
@app.get("/")
def home():
    return {"message": "Welcome to the Health Chatbot API with MongoDB!"}

# Add or Update User Health Data
@app.post("/add-health-data/")
def add_health_data(data: HealthData):
    try:
        # Insert or Update User Data
        user_data = {
            "username": data.username,
            "activity_level": data.activity_level,
            "miles_ran": data.miles_ran,
            "sleep_hours": data.sleep_hours,
            "calories": data.calories,
        }
        result = user_collection.update_one(
            {"username": data.username}, {"$set": user_data}, upsert=True
        )
        return {"message": "Health data added/updated successfully!", "matched_count": result.matched_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Retrieve User Health Data
@app.get("/get-health-data/{username}")
def get_health_data(username: str):
    user = user_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return {"user_data": user}

# Simple Chatbot Logic
@app.post("/chat/")
def chatbot_response(chat: ChatInput):
    query = chat.query.lower()
    response = ""

    # Simple Rules for Responses
    if "sleep" in query:
        response = "You should aim for 7-8 hours of sleep daily for better health."
    elif "exercise" in query:
        response = "Try to exercise for at least 30 minutes a day to stay fit."
    elif "calories" in query:
        response = "A balanced diet should have about 2000-2500 calories per day."
    else:
        response = "I'm not sure, but I'm here to help! Ask about sleep, exercise, or calories."

    # Store Chat Log in MongoDB
    chat_log = {"query": chat.query, "response": response}
    chat_collection.insert_one(chat_log)

    return {"query": chat.query, "response": response}

# Retrieve Chat Logs
@app.get("/chat-logs/")
def get_chat_logs():
    chats = list(chat_collection.find({}, {"_id": 0}))  # Exclude ObjectId
    return {"chat_logs": chats}