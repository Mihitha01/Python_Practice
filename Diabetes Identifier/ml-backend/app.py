
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os

# Create app
app = FastAPI()

# Enable CORS (VERY IMPORTANT for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load model & scaler with error handling
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = None
scaler = None
model_path = os.path.join(BASE_DIR, "models", "logistic_regression_model.pkl")
scaler_path = os.path.join(BASE_DIR, "models", "scaler.pkl")

def load_artifacts():
    global model, scaler
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    except Exception as e:
        print(f"Error loading model or scaler: {e}")
        model = None
        scaler = None

# FastAPI startup event
@app.on_event("startup")
def startup_event():
    load_artifacts()

# Test route
@app.get("/")
def home():
    return {"message": "Backend is running"}

# Pydantic model for input validation
class PredictRequest(BaseModel):
    Pregnancies: float
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: float

# Prediction route
@app.post("/predict")
def predict(data: PredictRequest):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model or scaler not loaded.")
    try:
        features = np.array([[
            data.Pregnancies,
            data.Glucose,
            data.BloodPressure,
            data.SkinThickness,
            data.Insulin,
            data.BMI,
            data.DiabetesPedigreeFunction,
            data.Age
        ]])
        features = scaler.transform(features)
        prediction = model.predict(features)[0]
        return {"prediction": int(prediction)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {e}")