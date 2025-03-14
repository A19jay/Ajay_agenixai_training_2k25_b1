import joblib
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

# Load the trained model, scaler, and encoder
model = joblib.load(r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\models\best_model.pkl")
scaler = joblib.load(r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\models\scaler.pkl")
encoder = joblib.load(r"C:\Users\ajayr\OneDrive\Desktop\agenix\Predicting_Energy_Consumption\models\encoder.pkl")

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Server Running Successfully"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input data from request
        data = request.get_json()

        # Convert input data to DataFrame
        df = pd.DataFrame(data)

        # Drop unnecessary columns
        if "BuildingID" in df.columns:
            df = df.drop(columns=["BuildingID"])

        # Encode categorical variables
        df_encoded = encoder.transform(df[["InsulationType", "RenewableEnergySource"]]).toarray()
        df_encoded = pd.DataFrame(df_encoded, columns=encoder.get_feature_names_out())

        # Drop original categorical columns and concatenate encoded features
        df = df.drop(columns=["InsulationType", "RenewableEnergySource"])
        df = pd.concat([df, df_encoded], axis=1)

        # Scale numerical features
        df_scaled = scaler.transform(df)

        # Make predictions
        predictions = model.predict(df_scaled)

        return jsonify({"message": "Prediction Successful", "predictions": predictions.tolist()})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("Server is running at http://127.0.0.1:5001/")
    app.run(debug=True, use_reloader=False, port=5001)  # Running on port 5001
