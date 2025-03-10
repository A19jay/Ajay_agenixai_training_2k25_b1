import os
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# Load the preprocessed data
data_path = "C:/Users/ajayr/OneDrive/Desktop/agenix/student_performance_analysis/processed/preprocessed_student_data.csv"
data = pd.read_csv(data_path)

# Ensure the target column exists
target_column = 'AcademicPerformanceStatus'
if target_column not in data.columns:
    raise ValueError(f"Error: Target column '{target_column}' not found in the dataset.")

# Define features (X) and target variable (y)
X = data.drop(columns=[target_column])
y = data[target_column]

# Split data into training and testing sets (same as model training)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load the trained model
model_path = "C:/Users/ajayr/OneDrive/Desktop/agenix/student_performance_analysis/models/trained_model.pkl"

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Error: Trained model not found at {model_path}. Train the model first.")

model = joblib.load(model_path)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Print evaluation metrics
print("\n Model Evaluation Results ")
print(f" Accuracy: {accuracy:.4f}")
print("\n Confusion Matrix:")
print(conf_matrix)
print("\n Classification Report:")
print(class_report)
