document.addEventListener("DOMContentLoaded", () => {
    chrome.storage.local.get("lastPrediction", (data) => {
      const resultDiv = document.getElementById("result");
      const list = document.getElementById("featuresList");
  
      if (data.lastPrediction) {
        const { url, prediction, features } = data.lastPrediction;
        resultDiv.innerHTML = `🔎 <b>${url}</b><br>Status: <span class="${prediction === 'Phishing' ? 'phishing' : 'safe'}">${prediction}</span>`;
  
        list.innerHTML = "";
        for (let key in features) {
          const li = document.createElement("li");
          li.textContent = `${key}: ${features[key]}`;
          list.appendChild(li);
        }
      } else {
        resultDiv.textContent = "No data yet.";
      }
    });
  });
  