document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.querySelector(".card-body");
    const form = document.querySelector('.custom-form');
    const promptInput = document.getElementById("prompt");
    const keyInput = document.getElementById("key");
    let sessionID = "unique_session_id";

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        const userPrompt = promptInput.value;
        const userKey = keyInput.value;

        fetch("/send-message", {
            method: "POST",
            body: JSON.stringify({ prompt: userPrompt, key: userKey, session_id: sessionID }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            const serverMessage = data.message;
            displayMessage(userPrompt, "user");
            displayMessage(serverMessage, "server");
        })
        .catch(error => console.error("Error:", error));
    });

    function displayMessage(message, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("card-text", "maxlines", "message", sender);
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
    }
});
