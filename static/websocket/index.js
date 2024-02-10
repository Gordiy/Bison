const chatSocket = new WebSocket('wss://bison-7663f2280730.herokuapp.com/ws/balance/');

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message = data['message'];
    console.log("Message:", message)

    // Handle incoming message
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('p');
    messageElement.textContent = message.balance;
    chatMessages.appendChild(messageElement);
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

// Send message to server
function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (message) {
        chatSocket.send(JSON.stringify({
            'message': message
        }));

        // Clear the input field
        messageInput.value = '';
    }
}