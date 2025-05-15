chrome.runtime.sendMessage(
    { action: "checkPhishing", url: window.location.href },
    response => {
        console.log("Phishing Detection Result:", response.result);
    }
);
