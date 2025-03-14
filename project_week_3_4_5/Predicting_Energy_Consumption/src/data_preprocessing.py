import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import os

# Load dataset
file_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\data\raw\building_energy_data.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"CSV file not found: {file_path}")

df = pd.read_csv(file_path)

# Drop unnecessary columns
df.drop(columns=["BuildingID", "EnergyConsumption"], errors="ignore", inplace=True)

# Handle missing values
for col in df.select_dtypes(include=["number"]).columns:
    df[col] = df[col].fillna(df[col].mean())  # Fill numeric columns with mean

for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].fillna(df[col].mode()[0])  # Fill categorical columns with mode

# One-Hot Encoding for categorical variables
categorical_cols = ["InsulationType", "RenewableEnergySource"]

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)  #  Fixing deprecated 'sparse' argument
encoded_features = encoder.fit_transform(df[categorical_cols])
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out())

# Drop original categorical columns and add encoded ones
df.drop(columns=categorical_cols, inplace=True)
df = pd.concat([df, encoded_df], axis=1)

# Feature Scaling
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df)
df_scaled = pd.DataFrame(scaled_features, columns=df.columns)

# Save processed data, encoder, and scaler
processed_data_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\processed\building_energy_data_cleaned.csv"
encoder_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\models\encoder.pkl"
scaler_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\models\scaler.pkl"

df_scaled.to_csv(processed_data_path, index=False)
joblib.dump(encoder, encoder_path)
joblib.dump(scaler, scaler_path)

print("Data preprocessing completed successfully!")
print(f"Processed data saved at: {processed_data_path}")
print(f"Encoder saved at: {encoder_path}")
print(f"Scaler saved at: {scaler_path}")