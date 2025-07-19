import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'You are connected!'
        }))

    async def receive(self, text_data):
        await self.send(text_data=json.dumps({
            'message': 'You sent: ' + text_data
        }))