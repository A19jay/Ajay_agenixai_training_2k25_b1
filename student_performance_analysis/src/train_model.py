import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load the preprocessed data
file_path = "C:/Users/ajayr/OneDrive/Desktop/agenix/student_performance_analysis/processed/preprocessed_student_data.csv"
data = pd.read_csv(file_path)

# Ensure the target column exists
target_column = 'AcademicPerformanceStatus'
if target_column not in data.columns:
    raise ValueError(f"Error: Target column '{target_column}' not found in the dataset.")

# Define features (X) and target variable (y)
X = data.drop(columns=[target_column])
y = data[target_column]

# Handle missing values in y
if y.isna().sum() > 0:
    if not y.mode().empty:
        y.fillna(y.mode()[0], inplace=True)
        print("Missing values in target variable filled with mode.")
    else:
        raise ValueError("Error: Mode could not be computed. The target variable contains only NaN values.")

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Define the model path
model_dir = "C:/Users/ajayr/OneDrive/Desktop/agenix/student_performance_analysis/models"
model_path = os.path.join(model_dir, "trained_model.pkl")

# Create the directory if it does not exist
os.makedirs(model_dir, exist_ok=True)

# Save the trained model
joblib.dump(model, model_path)

print("Model training completed and saved at:", model_path)




