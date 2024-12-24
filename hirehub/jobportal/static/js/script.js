let prompt = document.querySelector("#prompt");
let submitbtn = document.querySelector("#submit");
let chatContainer = document.querySelector(".chat-container");
const API_KEY = "AIzaSyBdVNTdrfjHvb-IKMBACdlkJzvd_r4SETE"; // Your API key here
const API_URL = `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key=${API_KEY}`;

let user = {
    data: null,
};

async function generateResponse(aiChatBox) {
    let text=aiChatBox.querySelector(".ai-chat-area")
    let requestOption = {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            contents: [{
                role: "user",
                parts: [{ text: user.data }]
            }]
        })
    };
    try {
        let response = await fetch(API_URL, requestOption);
        let data = await response.json();
     

        // Assuming the response contains the AI's reply in a specific format
        let aiResponse = data.candidates[0].contents.parts[0].text.replace(/\*\*(.*?)\*\*/g,"$1").trim()
        let html = `<img src="ai.png" alt="" id="aiImage" width="50">
                    <div class="ai-chat-area">${aiResponse}</div>`;
        aiChatBox.innerHTML = html; // Update the AI chat box with the response
        console.log(aiResponse);
    } catch (error) {
        console.log(error);
    }
    finally{
        chatContainer.scrollTo({top:chatContainer.scrollHeight,behavior:smooth})
    }
}

function createChatBox(html, classes) {
    let div = document.createElement("div");
    div.innerHTML = html;
    div.classList.add(classes); // Corrected from 'div.classes.add' to 'div.classList.add'
    return div;
}

function handleChatResponse(message) {
    user.data = message;
    let html = `<img src="user-6380868_1280.png" alt="" id="userImage" width="50">
                <div class="user-chat-area">${user.data}</div>`;
    prompt.value = ""; // Clear the input field
    let userChatBox = createChatBox(html, "user-chat-box");
    chatContainer.appendChild(userChatBox);
    chatContainer.scrollTo({top:chatContainer.scrollHeight,behavior:smooth})
    setTimeout(() => {
        let html = `<img src="ai.png" alt="" id="aiImage" width="50">
                    <div class="ai-chat-area">
                      <img src="C:\\Users\\huawei\\Desktop\\jobpro\\hirehub\\jobportal\\static\\images\\load.webp" alt="" class="load" width="50px">
                    </div>`;
        let aiChatBox = createChatBox(html, "ai-chat-box");
        chatContainer.appendChild(aiChatBox);
        generateResponse(aiChatBox);
    }, 600);
}

prompt.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && prompt.value.trim() !== "") { // Check for non-empty input
        handleChatResponse(prompt.value);
    }
})

submitbtn.addEventListener("click",()=>{
    handleChatResponse(prompt.value);
})