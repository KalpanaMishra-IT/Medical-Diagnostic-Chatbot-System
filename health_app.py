# === MongoDB Database Setup ===
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://ichikawakumiko0:8DCvkJISQ0CEb5ZM@cluster0.tywec.mongodb.net/")
db = client["health_app"]
users_collection = db["users"]

# Example user data (this can be extended further)
def initialize_user():
    user_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "weight": 70,
        "height": 170,
        "dob": "1995-05-15",
        "medical_history": "None",
        "activity_level": "medium",
        "health_metrics": []
    }
    users_collection.insert_one(user_data)

# Uncomment to initialize a user (run once):
# initialize_user()

# === FastAPI Backend ===
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import requests

app = FastAPI()

# Load ML model
try:
    model = joblib.load("model.pkl")
except FileNotFoundError:
    model = None

# Schemas
class HealthRequest(BaseModel):
    symptoms: str
    activity_level: str

class ChatbotRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Health Monitoring API is running."}

@app.post("/predict-health")
def predict_health(request: HealthRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    # Extract input
    symptoms = request.symptoms.lower()
    activity_level = request.activity_level.lower()

    try:
        input_data = np.array([len(symptoms), len(activity_level)]).reshape(1, -1)
        prediction = model.predict(input_data)
        result = {"prediction": "At Risk" if prediction[0] == 1 else "Healthy"}

        # Store result in MongoDB
        users_collection.update_one(
            {"username": "john_doe"},  # Replace with dynamic username
            {"$push": {"health_metrics": result}}
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing input: {str(e)}")

    return result

@app.post("/chatbot")
def chatbot_interaction(request: ChatbotRequest):
    user_message = request.message.lower()

    if "symptom" in user_message:
        response = "Can you describe your symptoms in detail?"
    elif "activity" in user_message:
        response = "How would you rate your activity level: low, medium, or high?"
    elif "predict" in user_message:
        response = "Please provide your symptoms and activity level to get a prediction."
    else:
        response = "I am here to help you with your health. Please tell me your symptoms or activity level."

    return {"response": response}

@app.get("/fetch-metrics")
def fetch_metrics():
    api_url = "https://openmhealth.org/api"  # Replace with actual Open mHealth API URL
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

