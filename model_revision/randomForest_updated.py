import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import json
import logging
from fastapi import FastAPI

# -----------------------------
# Setup logging
# -----------------------------
logging.basicConfig(level=logging.INFO)
logging.info("Starting model training...")

# -----------------------------
# Load and preprocess data
# -----------------------------
data = pd.read_csv("data/insurance.csv")
data = pd.get_dummies(data, drop_first=True)

X = data.drop("charges", axis=1)
y = data["charges"]

# Save feature columns for later preprocessing
feature_columns = list(X.columns)
with open("feature_columns.json", "w") as f:
    json.dump(feature_columns, f)

# -----------------------------
# Split data and train model
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# Evaluate model
# -----------------------------
y_pred = model.predict(X_test)
logging.info(f"MSE: {mean_squared_error(y_test, y_pred):.2f}")
logging.info(f"R2 Score: {r2_score(y_test, y_pred):.2f}")

# -----------------------------
# Save the model for deployment
# -----------------------------
joblib.dump(model, "random_forest_model.pkl")
logging.info("Model saved as random_forest_model.pkl")

# -----------------------------
# Prediction preprocessing function
# -----------------------------
def preprocess_input(input_df):
    """
    Preprocess incoming data to match training features.
    """
    # Load saved feature columns
    with open("feature_columns.json", "r") as f:
        feature_columns = json.load(f)
    
    # One-hot encode
    input_df = pd.get_dummies(input_df, drop_first=True)
    
    # Add missing columns
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    
    # Ensure correct column order
    input_df = input_df[feature_columns]
    return input_df

# -----------------------------
# Prediction function
# -----------------------------
def predict_charges(input_data: dict):
    """
    input_data: dict containing a single record e.g.
    {
        "age": 30,
        "sex": "male",
        "bmi": 25.0,
        "children": 1,
        "smoker": "yes",
        "region": "northwest"
    }
    """
    df = pd.DataFrame([input_data])
    processed_df = preprocess_input(df)
    prediction = model.predict(processed_df)
    return prediction[0]

# -----------------------------
# Optional: FastAPI setup
# -----------------------------
app = FastAPI()
logging.info("API ready for predictions...")

@app.post("/predict")
def api_predict(data: dict):
    try:
        result = predict_charges(data)
        return {"prediction": result}
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return {"error": str(e)}

