from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import socket
import whois
from urllib.parse import urlparse
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load the model
with open("phishing_model.pkl", "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
scaler = model_data["scaler"]
feature_names = model_data["features"]

def extract_features(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc or parsed_url.path
        if domain.startswith("www."):
            domain = domain[4:]

        # DNS_Record
        try:
            socket.gethostbyname(domain)
            dns_record = 0  # Safe
        except:
            dns_record = 1  # Risky

        # WHOIS info
        try:
            whois_info = whois.whois(domain)
            creation_date = whois_info.creation_date
            expiration_date = whois_info.expiration_date

            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]

            domain_age = 1 if (creation_date is None or (datetime.now() - creation_date).days < 180) else 0
            domain_end = 1 if (expiration_date is None or (expiration_date - datetime.now()).days < 180) else 0
        except:
            domain_age = 1
            domain_end = 1

        # Features based on URL string
        features = {
            "Have_IP": 1 if any(char.isdigit() for char in domain.split('.')) else 0,
            "Have_At": 1 if "@" in url else 0,
            "URL_Length": len(url),
            "URL_Depth": parsed_url.path.count("/"),
            "Redirection": 1 if "//" in url[8:] else 0,
            "https_Domain": 1 if url.startswith("https://") else 0,
            "TinyURL": 1 if len(url) < 20 else 0,
            "Prefix/Suffix": 1 if "-" in domain else 0,
            "DNS_Record": dns_record,
            "Web_Traffic": 1,  # Optional: Use Alexa or keep as 1 if not checking
            "Domain_Age": domain_age,
            "Domain_End": domain_end,
            "iFrame": 0,
            "Mouse_Over": 0,
            "Right_Click": 0,
            "Web_Forwards": 0
        }

        input_df = pd.DataFrame([features], columns=feature_names)
        return input_df

    except Exception as e:
        raise ValueError(f"Feature extraction failed: {str(e)}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        input_data = extract_features(url)
        input_scaled = scaler.transform(input_data)
        result = model.predict(input_scaled)[0]
        prediction = "Phishing" if result == 1 else "Legitimate"

        raw_features = input_data.iloc[0].to_dict()
        feature_risks = {k: "⚠️ Risky" if v == 1 else "✅ Safe" for k, v in raw_features.items()}

        return jsonify({
            "prediction": prediction,
            "features": feature_risks
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
