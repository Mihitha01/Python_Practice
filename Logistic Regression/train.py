import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

data = pd.read_csv("data/diabetes.csv")

x = data.drop("Outcome", axis=1)
y = data["Outcome"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(x_train)
X_test = scaler.transform(x_test)

model = LogisticRegression(max_iter=1000, solver='liblinear')  # Increase max_iter to ensure convergence
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print(f"Confusion Matrix: {conf_matrix}")
print(f"Classification Report: {class_report}")

joblib.dump(model, "D:/Python/Logistic Regression/models/logistic_regression_model.pkl")
joblib.dump(scaler, "D:/Python/Logistic Regression/models/scaler.pkl")

print("saved model and scaler successfully.")
