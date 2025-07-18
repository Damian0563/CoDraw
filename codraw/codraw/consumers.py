import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'message': 'You are connected!'
        }))

    def receive(self, text_data):
        self.send(text_data=json.dumps({
            'message': 'You sent: ' + text_data
        }))