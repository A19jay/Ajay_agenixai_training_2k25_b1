from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd
import os
from waitress import serve  # Production server

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), "../models/trained_model.pkl")
model = joblib.load(model_path)

# Define the prediction route
@app.route("/predict", methods=["POST"])
def predict_student_performance():
    try:
        data = request.json
        input_data = pd.DataFrame([data.values()], columns=data.keys())

        # Make predictions
        prediction = model.predict(input_data)[0]

        return jsonify({"prediction": int(prediction)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Root route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Student Performance Analysis API"})

# Favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Run the production server
if __name__ == "__main__":
    print("Starting Flask server...")
    serve(app, host="127.0.0.1", port=5001)
