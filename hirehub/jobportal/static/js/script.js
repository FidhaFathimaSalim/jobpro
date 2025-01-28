let prompt=document.querySelector('#prompt')
let chatContainer=document.querySelector('.chat-container')
let sendButton = document.querySelector('#submit');

const Api_Url="https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyAVlqYB5MSmxTKK-aTgEopWf85tVG3r0qM"
let user={
    data:null,
}
async function generateResponse(aiChatBox) {
let text=aiChatBox.querySelector(".ai-chat-area")
let RequestOption={
    method:"POST",
    headers:{'Content-Type': 'application/json'},
    body:JSON.stringify({
        "contents": [
            { "parts":[{"text": user.data}

            ]
        }]
    })
}
try{
    let response= await fetch(Api_Url,RequestOption)
    let data=await response.json()
    let apiResponse=data.candidates[0].content.parts[0].text.replace(/\*\*(.*?)\*\*/g,"$1").trim()
    text.innerHTML=apiResponse
}
catch(error){
    console.log(error);
}
finally{
    chatContainer.scrollTo({top:chatContainer.scrollHeight,behavior:"smooth"})
}
}

function createChatBox(html,classes){
    let div=document.createElement("div")
    div.innerHTML=html
    div.classList.add(classes)
    return div
}

function handlechatResponse(message){
    user.data=message
    let html=`<img src="{% static 'images/user-6380868_1280.png' %}" alt="" id="userImage" width="100">
<div class="user-chat-area">
${user.data}
</div>`
prompt.value=""
let userChatBox=createChatBox(html,"user-chat-box")
chatContainer.appendChild(userChatBox)
chatContainer.scrollTo({top:chatContainer.scrollHeight,behavior:"smooth"})
setTimeout(()=>{
    let html = `
    <img src="{% static 'images/ai.png' %}" alt="" id="aiImage" width="70">
    <div class="ai-chat-area">
        <img src="{% static 'images/load.webp' %}" alt="" class="load" width="50px">
    </div>`
let aiChatBox=createChatBox(html,"ai-chat-box")
chatContainer.appendChild(aiChatBox)
generateResponse(aiChatBox)
},600)
}

function createChatBox(html,classes){
    let div=document.createElement("div")
    div.innerHTML=html
    div.classList.add(classes)
    return div
}

prompt.addEventListener("keydown",(e)=>{
    if(e.key=="Enter"){
        handlechatResponse(prompt.value)
    }
})
sendButton.addEventListener("click", () => {
    if (prompt.value.trim() !== "") {
        handlechatResponse(prompt.value);
    }
});