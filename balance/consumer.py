import json

from channels.generic.websocket import WebsocketConsumer


class BalanceConsumer(WebsocketConsumer):
    def connect(self):
        """Accept client connection."""
        self.accept()

    def disconnect(self, close_code):
        """Disable disconnect method."""
        pass

    def receive(self, text_data):
        """Handle incoming message."""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': message
        }))