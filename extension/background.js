chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url.startsWith("http")) {
      checkUrlWithBackend(tab.url);
    }
  });
  
  function checkUrlWithBackend(url) {
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    })
      .then(response => response.json())
      .then(data => {
        const prediction = data.prediction;
  
        // Save result to chrome storage
        chrome.storage.local.set({ lastPrediction: { url, prediction, features: data.features } });
  
        if (prediction === "Phishing") {
          chrome.notifications.create({
            type: "basic",
            title: "⚠️ Phishing Detected!",
            message: `The website ${url} appears to be suspicious.`,
            iconUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Warning_icon.svg/2048px-Warning_icon.svg.png"
          });
        } else {
          console.log("Website is legitimate:", url);
        }
      })
      .catch(err => {
        console.error("Error checking phishing:", err);
      });
  }
  