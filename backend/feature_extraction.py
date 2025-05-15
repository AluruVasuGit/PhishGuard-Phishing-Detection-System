import re 
import whois
import urllib.parse
import socket
import requests
import pandas as pd
from datetime import datetime

# Define feature names including "Result"
feature_names = [
    "_id", "assets_downloaded", "brands", "domain", "features.css",
    "features.html", "features.text", "folder_path", "language", "protocol",
    "remote_ip_address", "remote_ip_asn", "remote_ip_country", "remote_ip_domain",
    "remote_ip_isp", "remote_ip_isp_org", "scan_date", "security_issuer",
    "security_protocol", "Result", "security_valid_from", "security_valid_to",
    "url", "whois_domain_age", "whois_raw_text", "whois_registrar",
    "whois_registrar_url", "whois_registry_created_at",
    "whois_registry_expired_at", "whois_registry_updated_at"
]

# Feature extraction function
def extract_features(row):
    url = row["url"]
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc
    features = []
    
    # Feature: Having IP address in URL
    features.append(1 if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain) else 0)
    
    # Feature: URL Length
    features.append(len(url))
    
    # Feature: Shortening Service
    features.append(1 if any(short in url for short in ["bit.ly", "tinyurl", "goo.gl"]) else 0)
    
    # Feature: Having '@' Symbol
    features.append(1 if "@" in url else 0)
    
    # Feature: SSL Final State
    try:
        response = requests.get(url, timeout=5)
        features.append(1 if response.url.startswith("https") else 0)
    except:
        features.append(0)
    
    # Feature: Domain Registration Length
    try:
        domain_info = whois.whois(domain)
        expiration_date = domain_info.expiration_date[0] if isinstance(domain_info.expiration_date, list) else domain_info.expiration_date
        features.append(1 if (expiration_date - datetime.now()).days > 365 else 0)
    except:
        features.append(0)
    
    # Feature: DNS Record
    try:
        socket.gethostbyname(domain)
        features.append(1)
    except:
        features.append(0)
    
    # Add other dataset columns as features
    for col in feature_names:
        if col in row.index:
            features.append(row[col])
        else:
            features.append(0)
    
    return dict(zip(feature_names, features))

# Load dataset and process features
df = pd.read_csv("dataset/phishing.csv")  
df.columns = df.columns.str.strip()  # Remove extra spaces from column names
print("Column Names After Stripping Spaces:", df.columns)  # Debugging

df["features"] = df.apply(lambda row: extract_features(row), axis=1)
df = df.join(pd.DataFrame(df.pop("features").tolist()))

# Save processed dataset with all features including "Result"
df.to_csv("dataset/processed_phishing.csv", index=False)

print("Processed dataset saved successfully with 'Result' column!")
