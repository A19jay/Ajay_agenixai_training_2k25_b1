import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(input_path, output_path):
    # Load the dataset
    data = pd.read_csv(input_path)
    
    # Drop unnecessary columns (if any, like StudentID)
    if 'StudentID' in data.columns:
        data.drop(columns=['StudentID'], inplace=True)
    
    # Handle missing values
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = data[col].fillna(data[col].mode()[0])  # Fill categorical with mode
    for col in data.select_dtypes(include=['number']).columns:
        data[col] = data[col].fillna(data[col].mean())  # Fill numeric with mean
    
    # Encode categorical variables
    label_encoders = {}
    categorical_columns = ['Gender', 'SocioeconomicStatus', 'ClassParticipation', 'AcademicPerformanceStatus']
    for col in categorical_columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = dict(zip(le.classes_, le.transform(le.classes_)))
    
    # Feature Scaling
    scaler = StandardScaler()
    numerical_features = ['Age', 'Grades', 'Attendance', 'TimeSpentOnHomework']
    data[numerical_features] = scaler.fit_transform(data[numerical_features])
    
    # Save the preprocessed dataset
    data.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    input_csv = "C:/Users/ajayr/OneDrive/Desktop/agenix/student_performance_analysis/raw/student_performance_data.csv"
    output_csv = "C:/Users/ajayr/OneDrive/Desktop/agenix/student_performance_analysis/processed/preprocessed_student_data.csv"
    preprocess_data(input_csv, output_csv)
