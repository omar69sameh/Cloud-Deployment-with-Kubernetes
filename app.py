from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model and encoders
model = joblib.load('recidivism_model.pkl')
encoders = joblib.load('label_encoders.pkl')
feature_names = joblib.load('feature_names.pkl')

@app.route('/healthz', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Encode categorical features
        sex_encoded = encoders['sex'].transform([data['sex']])[0]
        legal_encoded = encoders['legal'].transform([data['legal_status']])[0]
        marital_encoded = encoders['marital'].transform([data['marital_status']])[0]
        
        # Create feature array
        features = [
            data['age'],
            sex_encoded,
            legal_encoded,
            marital_encoded,
            data['raw_score']
        ]
        
        # Make prediction
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0]
        
        return jsonify({
            "high_risk_prediction": int(prediction),
            "risk_level": "High Risk (7-10)" if prediction == 1 else "Low-Medium Risk (1-6)",
            "probability": {
                "low_medium_risk": float(probability[0]),
                "high_risk": float(probability[1])
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Recidivism Risk Prediction API",
        "endpoints": {
            "/healthz": "Health check",
            "/predict": "POST - Predict recidivism risk"
        },
        "example_request": {
            "age": 25,
            "sex": "Male",
            "legal_status": "Pretrial",
            "marital_status": "Single",
            "raw_score": 5
        }
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)