from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (important for frontend requests)

# Function to find disease based on user symptoms
def find_disease(user_symptoms):
    conn = sqlite3.connect('diseases.db')
    cursor = conn.cursor()

    cursor.execute("SELECT disease_name, symptoms, advice FROM diseases")
    diseases = cursor.fetchall()

    conn.close()

    # Normalize user symptoms
    user_symptoms = user_symptoms.lower()

    best_match = None
    max_matches = 0

    for disease_name, symptoms, advice in diseases:
        # Break symptoms stored in DB into a list
        symptom_list = [sym.strip().lower() for sym in symptoms.split(',')]
        matches = 0

        # Check if any stored symptom appears in user input
        for symptom in symptom_list:
            if symptom in user_symptoms:
                matches += 1

        # Keep track of disease with maximum symptom matches
        if matches > max_matches:
            best_match = (disease_name, advice)
            max_matches = matches

    # If no match found, return "Unknown"
    if best_match:
        return {'disease': best_match[0], 'advice': best_match[1]}
    else:
        return {'disease': "Unknown", 'advice': "Please consult a healthcare provider."}

# API endpoint to receive POST request from frontend
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_symptoms = data.get('symptoms', '')
    result = find_disease(user_symptoms)
    return jsonify(result)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
