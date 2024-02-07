"""Consumer for balance app."""
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class BalanceConsumer(AsyncWebsocketConsumer):
    group_name = 'websocket.connect'

    async def connect(self):
        """Accept client connection."""
        await self.accept()

        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, close_code):
        """Disable disconnect method."""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """Handle incoming message."""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        print(message)
        await self.send_message_to_all(message)

    async def send_message_to_all(self, message):
        """Send message to all connected clients."""
        connected_channels = await self.get_connected_channels()
        for connected_channel in connected_channels:
            await self.channel_layer.send(
                connected_channel,
                {
                    'type': 'send_balance_message',
                    'message': message
                }
            )

    async def get_connected_channels(self):
        """Get list of connected channels."""
        connected_channels = set()
        for group_name, channels in self.channel_layer.groups.items():
            if group_name == self.group_name:
                connected_channels.update(channels)
        return connected_channels

    async def send_balance_message(self, event):
        """Send balance message to the client."""
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
