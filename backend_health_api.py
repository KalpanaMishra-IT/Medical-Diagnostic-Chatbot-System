from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Define request schema
class HealthRequest(BaseModel):
    symptoms: str
    activity_level: str

# Define your PyTorch model class (adjust according to your actual model)
class HealthModel(torch.nn.Module):
    def __init__(self):
        super(HealthModel, self).__init__()
        self.fc = torch.nn.Linear(2, 1)  # Adjust input/output dimensions as per your model

    def forward(self, x):
        return self.fc(x)

# Load pre-trained PyTorch model
model = HealthModel()
try:
    model.load_state_dict(torch.load("model.pth"))
    model.eval()
except FileNotFoundError:
    model = None

@app.get("/")
def read_root():
    return {"message": "Health Monitoring API is running."}

@app.post("/predict-health")
def predict_health(request: HealthRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded. Please ensure 'model.pth' is in the correct directory.")

    # Extract input data
    symptoms = request.symptoms.lower()
    activity_level = request.activity_level.lower()

    # Preprocess the input (adjust based on your model's requirements)
    try:
        input_data = np.array([len(symptoms), len(activity_level)]).reshape(1, -1)
        input_tensor = torch.tensor(input_data, dtype=torch.float32)
        with torch.no_grad():
            prediction = model(input_tensor).numpy()
        result = {"prediction": int(prediction[0][0])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing input: {str(e)}")

    return result
