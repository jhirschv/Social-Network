document.addEventListener('DOMContentLoaded', function() {

    let loc = window.location;
    let wsStart = 'wss://';
    let endpoint = wsStart + loc.host + loc.pathname;

    const socket = new WebSocket(endpoint)

    socket.onopen = function(e) {
        console.log('Chat socket opened successfully');
        // Perform any action once the WebSocket connection is opened.
    };

    socket.onmessage = function(e) {
        console.log('message');
        // ... handle incoming messages ...
        const data = JSON.parse(e.data);
        // Code to handle incoming message
        displayMessage(data.message);
    };

    socket.onerror = function(e) {
        console.log('error');
        // ... handle incoming messages ...
    };

    socket.onclose = function(e) {
        console.log('Chat socket closed unexpectedly');
        // Handle WebSocket closing
    };

    document.querySelector('#sendMessage').onclick = function(e) {
        const messageInputDom = document.querySelector('#messageInput');
        const message = messageInputDom.value;
        socket.send(JSON.stringify({'message': message}));
        messageInputDom.value = '';
    };

    function displayMessage(message) {
        // Append message to the chat
        // Example: appending to a div with id 'chatLog'
        const chatLog = document.getElementById('chatMessage');
        chatLog.innerHTML += `<div>${message}</div>`;
    }

    // ... code for sending messages ...
});