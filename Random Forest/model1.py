import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

try:
    df = pd.read_csv('sri_lanka_flood_risk_dataset_25000.csv')
    print("Dataset loaded successfully")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Drop target and non-predictive columns
    X = df.drop(columns=['flood_risk_score', 'record_id', 'place_name', 'generation_date', 'reason_not_good_to_live'])
    y = df['flood_risk_score']
    # One-hot encode categorical columns
    X = pd.get_dummies(X)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    print("Training model...")
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    print("R2 Score:", r2_score(y_test, y_pred))
except Exception as e:
    print(f"Error: {e}")