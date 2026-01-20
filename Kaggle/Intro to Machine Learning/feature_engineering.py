import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("dataset.csv")

# -----------------------------
# 2. Handle missing values
# -----------------------------

# Fill numerical missing values with mean
num_cols = df.select_dtypes(include=["int64", "float64"]).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].mean())

# Fill categorical missing values with mode
cat_cols = df.select_dtypes(include=["object"]).columns
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# -----------------------------
# 3. Encode categorical features
# -----------------------------

label_encoder = LabelEncoder()
for col in cat_cols:
    df[col] = label_encoder.fit_transform(df[col])

# -----------------------------
# 4. Feature creation (example)
# -----------------------------

# Example: create a new feature using existing ones
# (Modify this based on your dataset)
if "total_price" in df.columns and "quantity" in df.columns:
    df["price_per_item"] = df["total_price"] / df["quantity"]

# -----------------------------
# 5. Feature scaling
# -----------------------------

scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# -----------------------------
# 6. Split features & target
# -----------------------------

X = df.drop("target", axis=1)  # replace "target" with your label column
y = df["target"]

# -----------------------------
# 7. Train-test split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Feature Engineering Completed ✅")
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
