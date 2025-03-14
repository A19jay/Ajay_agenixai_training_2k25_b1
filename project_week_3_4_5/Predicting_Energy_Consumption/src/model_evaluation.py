import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os

# File paths
model_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\models\best_model.pkl"
scaler_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\models\scaler.pkl"
encoder_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\models\encoder.pkl"
train_data_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\processed\building_energy_data_cleaned.csv"
test_data_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\processed\building_energy_data_cleaned.csv"

# Check if files exist
for path in [model_path, scaler_path, encoder_path, test_data_path, train_data_path]:
    if not os.path.exists(path):
        raise FileNotFoundError(f" File not found: {path}")

# Load model, scaler, and encoder
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)
encoder = joblib.load(encoder_path)

# Load training and test datasets
df_train = pd.read_csv(train_data_path)
df_test = pd.read_csv(test_data_path)

# Drop 'BuildingID' if it exists
df_train.drop(columns=["BuildingID"], errors="ignore", inplace=True)
df_test.drop(columns=["BuildingID"], errors="ignore", inplace=True)

# Extract features and target variable
X_train = df_train.drop(columns=["EnergyConsumption"], errors="ignore")
X_test = df_test.drop(columns=["EnergyConsumption"], errors="ignore")
y_test = df_test["EnergyConsumption"] if "EnergyConsumption" in df_test.columns else None

# Categorical column handling
categorical_cols = ["InsulationType", "RenewableEnergySource"]

# **🔹 Check if categorical columns exist in X_train**
missing_categorical_cols = [col for col in categorical_cols if col not in X_train.columns]

if missing_categorical_cols:
    print(f"⚠️ Warning: Missing categorical columns in X_train: {missing_categorical_cols}")
else:
    # Encode categorical features using the same encoder from training
    X_train_encoded = encoder.transform(X_train[categorical_cols])
    X_test_encoded = encoder.transform(X_test[categorical_cols])

    # Convert encoded features into DataFrame
    X_train_encoded_df = pd.DataFrame(X_train_encoded, columns=encoder.get_feature_names_out(), index=X_train.index)
    X_test_encoded_df = pd.DataFrame(X_test_encoded, columns=encoder.get_feature_names_out(), index=X_test.index)

    # Drop original categorical columns and add encoded ones
    X_train.drop(columns=categorical_cols, inplace=True)
    X_test.drop(columns=categorical_cols, inplace=True)

    X_train = pd.concat([X_train, X_train_encoded_df], axis=1)
    X_test = pd.concat([X_test, X_test_encoded_df], axis=1)

# **Ensure X_test has the same columns as X_train**
missing_cols = set(X_train.columns) - set(X_test.columns)
extra_cols = set(X_test.columns) - set(X_train.columns)

# Add missing columns with zero values
for col in missing_cols:
    X_test[col] = 0

# Drop extra columns that shouldn't exist
X_test = X_test[X_train.columns]

# Feature Scaling
X_test_scaled = scaler.transform(X_test)

# Model Predictions
y_pred = model.predict(X_test_scaled)

# Evaluation Metrics
if y_test is not None:
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(" Model Evaluation Completed")
    print(f" MAE (Mean Absolute Error): {mae:.4f}")
    print(f" MSE (Mean Squared Error): {mse:.4f}")
    print(f" RMSE (Root Mean Squared Error): {rmse:.4f}")
    print(f" R² Score: {r2:.4f}")
else:
    print(" Warning: No 'EnergyConsumption' column found in test data. Model evaluation skipped.")

