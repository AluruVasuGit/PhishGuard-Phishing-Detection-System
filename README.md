# 🛡️ PhishGuard – Phishing Website Detection System

PhishGuard is an intelligent phishing detection system that identifies potentially malicious URLs using machine learning techniques. It includes a dynamic web interface built with Flask and JavaScript, and a browser extension for real-time phishing alerts.

---

## 🚀 Features

- 🔍 Real-time URL analysis using a trained ML model
- 🌐 Flask-based web app with AJAX-powered user interface
- 📊 Risk indicators based on URL feature analysis
- 📁 URL history tracking
- 🧩 Browser extension that auto-detects phishing attempts

---

## 🧠 Tech Stack

- **Frontend:** HTML, CSS, JavaScript (AJAX)
- **Backend:** Python, Flask
- **ML Model:** Scikit-learn (Random Forest / Decision Tree / etc.)
- **Others:** Browser Extension (Manifest V3), Bootstrap (optional), JSON

---

## 📂 Project Structure
PhishGuard/
│
├── static/ # CSS, JavaScript
├── templates/ # HTML files
├── extension/ # Chrome extension files
├── model/ # Trained ML model (.pkl)
├── app.py # Flask backend
├── features.py # Feature extraction logic
├── requirements.txt # Python dependencies
└── README.md # Project overview


---

## 🧪 How It Works

1. **User submits a URL** via the web interface or visits a site via browser.
2. **Feature extraction** is performed on the URL (e.g., domain age, use of IP, URL length).
3. The **trained ML model** classifies it as *phishing* or *legitimate*.
4. If phishing:
   - Web app shows warning with risk indicators.
   - Extension shows a popup notification and icon alert.

---

## ⚙️ Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/PhishGuard.git
cd PhishGuard

2. Create and Activate Virtual Environment

python -m venv env
source env/bin/activate      # On Windows: env\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Run the Flask App
python app.py

5. Load Browser Extension

Go to chrome://extensions/
Enable Developer Mode
Click "Load unpacked"
Select the /extension/ folder


Use Cases

Security Operations Centers (SOC)
Web traffic monitoring tools
Browser safety plugins
Awareness tools for non-technical users



