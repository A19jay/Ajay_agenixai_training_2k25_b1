import pandas as pd
import numpy as np
import joblib
import os
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Paths
train_data_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\processed\building_energy_data_cleaned.csv"
model_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\models\best_model.pkl"
encoder_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\models\encoder.pkl"
scaler_path = r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\models\scaler.pkl"

# Check if training data exists
if not os.path.exists(train_data_path):
    raise FileNotFoundError(f" Training data not found: {train_data_path}")

# Load dataset
df = pd.read_csv(train_data_path)

# Drop 'BuildingID' if it exists
df.drop(columns=["BuildingID"], errors="ignore", inplace=True)

# Split into features and target variable
X = df.drop(columns=["EnergyConsumption"], errors="ignore")
y = df["EnergyConsumption"]

# Categorical columns
categorical_cols = ["InsulationType", "RenewableEnergySource"]

# Handle missing categorical columns
missing_categorical_cols = [col for col in categorical_cols if col not in X.columns]

if missing_categorical_cols:
    print(f" Warning: Missing categorical columns: {missing_categorical_cols}")
else:
    # One-Hot Encoding
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    X_encoded = encoder.fit_transform(X[categorical_cols])

    # Convert to DataFrame
    X_encoded_df = pd.DataFrame(X_encoded, columns=encoder.get_feature_names_out(), index=X.index)

    # Drop original categorical columns and add encoded ones
    X.drop(columns=categorical_cols, inplace=True)
    X = pd.concat([X, X_encoded_df], axis=1)

# Train-test split (80-20)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Model definition
xgb_model = XGBRegressor(objective="reg:squarederror", random_state=42)

# Hyperparameter tuning using GridSearchCV
param_grid = {
    "n_estimators": [100, 200, 300],
    "learning_rate": [0.01, 0.1, 0.2],
    "max_depth": [3, 5, 7],
}

grid_search = GridSearchCV(xgb_model, param_grid, scoring="r2", cv=3, verbose=1, n_jobs=-1)
grid_search.fit(X_train_scaled, y_train)

# Best model
best_model = grid_search.best_estimator_

# Save best model, encoder, and scaler
joblib.dump(best_model, model_path)
joblib.dump(encoder, encoder_path)
joblib.dump(scaler, scaler_path)

# Predictions on validation set
y_pred = best_model.predict(X_val_scaled)

# Evaluation metrics
mae = mean_absolute_error(y_val, y_pred)
mse = mean_squared_error(y_val, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_val, y_pred)

# Print results
print("\n Model Training Completed Successfully!")
print(f"Best Hyperparameters: {grid_search.best_params_}")
print(f"MAE (Mean Absolute Error): {mae:.4f}")
print(f"MSE (Mean Squared Error): {mse:.4f}")
print(f"RMSE (Root Mean Squared Error): {rmse:.4f}")
print(f"R² Score: {r2:.4f}")

print(f"\n Model saved at: {model_path}")
print(f" Encoder saved at: {encoder_path}")
print(f" Scaler saved at: {scaler_path}")