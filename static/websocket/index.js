const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/balance/');

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data['message'];
    console.log('message')
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

function sendMessage(message) {
    chatSocket.send(JSON.stringify({
        'message': message
    }));
}