import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load the preprocessed data
input_file = "C:/Users/ajayr/OneDrive/Desktop/agenix/student_performance_analysis/processed/preprocessed_student_data.csv"
data = pd.read_csv(input_file)

# Encode categorical variables
categorical_columns = ['Gender', 'SocioeconomicStatus', 'ClassParticipation']
label_encoders = {}

for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = dict(zip(le.classes_, le.transform(le.classes_)))  # Store mappings for future use

# Convert target variable to binary format
data['AcademicPerformanceStatus'] = data['AcademicPerformanceStatus'].map({'Pass': 1, 'Fail': 0})

# Feature Scaling (Normalize numerical features)
scaler = StandardScaler()
numerical_columns = ['Age', 'Grades', 'Attendance', 'TimeSpentOnHomework']
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

# Feature Engineering: Creating new features
data['EngagementScore'] = (data['TimeSpentOnHomework'] * 0.5) + (data['Attendance'] * 0.5)

# Save the transformed dataset
output_file = "C:/Users/ajayr/OneDrive/Desktop/agenix/student_performance_analysis/processed/feature_engineered_student_data.csv"
data.to_csv(output_file, index=False)

print(f"Feature Engineering completed. Data saved to {output_file}")
