let prompt=document.querySelector("#prompt")
let chatContainer=document.querySelector(".chat-container")
const API_KEY = "AIzaSyBdVNTdrfjHvb-IKMBACdlkJzvd_r4SETE"; // Your API key here
const API_URL = `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key=${API_KEY}`;

let user={
    data:null,
}

async function generateResponse(aiChatBox) {

   let RequestOption={
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            contents: [{ 
                role: "user", 
                parts: [{ text: userMessage }] 
              }] 
            })
   }
    

 let response=fetch(API_URL,RequestOption)


}


function createChatBox(html,classes){
    let div=document.createElement("div")
    div.innerHTML=html
    div.classes.add(classes)
    return div
}


function handlechatResponse(message){
    let html='<img src="user-6380868_1280.png"alt="" id="userImage" width="50">
<div class="user-chat-area">
${message}
</div>'
prompt.value=" "
let userChatBox=createChatBox(html,"user-chat-box")
chatContainer.appendChild(userChatBox)

setTimeout(()=>{
let html='<img src="ai.png"alt="" id="aiImage" width="50">
    <div class="ai-chat-area">
      <img src="C:\Users\huawei\Desktop\jobpro\hirehub\jobportal\static\images\load.webp" alt="" class="load" width="50px">
    </div>'
    let aiChatBox=createChatBox(html,"ai-chat-box")
    chatContainer.appendChild(aiChatBox)
    generateResponse(aiChatBox)

},600)
}



prompt.addEventListener("keydown",(e)=>{
    if(e.key=="Enter"){
       handlechatResponse(prompt.value)
    }
    
})