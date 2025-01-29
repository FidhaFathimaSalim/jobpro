let prompt = document.querySelector('#prompt');
let chatContainer = document.querySelector('.chat-container');
let sendButton = document.querySelector('#submit');

const apiUrl = "/hirebot/";  

let user = {
    data: null,
};

function generateResponse(aiChatBox) {
    let text = aiChatBox.querySelector(".ai-chat-area");

    // Prepare data to send to Django
    let requestData = {
        'message': user.data
    };

    // Send the message to Django using Fetch API
    fetch(apiUrl, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        let apiResponse = data.response;
        text.innerHTML = apiResponse;
    })
    .catch(error => {
        console.error('Error:', error);
        text.innerHTML = "Sorry, something went wrong.";
    })
    .finally(() => {
        chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: "smooth" });
    });
}

function createChatBox(html, classes) {
    let div = document.createElement("div");
    div.innerHTML = html;
    div.classList.add(classes);
    return div;
}

function handleChatResponse(message) {
    user.data = message;
    let html = `<div class="user-chat-area">${user.data}</div>`;
    prompt.value = "";
    let userChatBox = createChatBox(html, "user-chat-box");
    chatContainer.appendChild(userChatBox);
    chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: "smooth" });

    setTimeout(() => {
        let html = `<div class="ai-chat-area"></div>`;
        let aiChatBox = createChatBox(html, "ai-chat-box");
        chatContainer.appendChild(aiChatBox);
        generateResponse(aiChatBox);
    }, 600);
}

prompt.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        handleChatResponse(prompt.value);
    }
});

sendButton.addEventListener("click", () => {
    if (prompt.value.trim() !== "") {
        handleChatResponse(prompt.value);
    }
});
