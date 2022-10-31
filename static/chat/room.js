
console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);
const userName = JSON.parse(document.getElementById('userName').textContent);

// if (created){
//     alert('created this room')
//     }
//     else{
//         alert('joined this room')
//     }



let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;

    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsersSelector.appendChild(newOption);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};




chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    
    chatSocket.send(JSON.stringify({
        "command" : 'chat_message' , 
        "message": chatMessageInput.value,
        "user_name": userName,
        "room_name": roomName,
    }));
    chatMessageInput.value = "";
};



let chatSocket = null;

function connect() {
    
    const protocol = location.protocol == 'http:' ? 'ws:' : 'wss:';
    chatSocket = new WebSocket(protocol + "//" + window.location.host + "/ws/chat/" + roomName + "/" + userName +"/");
    
    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 6000);
    };


    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case "chat_message":
                console.log('chat_message' , data)
                chatLog.value += data.message + "\n";
                break;

            case "user_list":
                    for (let i = 0; i < data.users.length; i++) {
                        if(data.users[i] != userName)
                            onlineUsersSelectorAdd(data.users[i]);
                    }
                    break;

            case "user_join":
                if( data.user_name != userName  ){

                 alert(data.user_name + " is joined the room")
                }

                    // chatLog.value += data.user + " joined the room.\n";
                    // onlineUsersSelectorAdd(data.user);
                break;

            case "user_leave":
                    chatLog.value += data.user + " left the room.\n";
                    onlineUsersSelectorRemove(data.user);
                    break;
            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}

connect();
