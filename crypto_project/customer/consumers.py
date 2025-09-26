import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PersonalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.group_name = f'user_{self.user_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def send_personal_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
#
# class CustomerConsumer(WebsocketConsumer):
#     groups = ["bets"]
#
#     def connect(self):
#         self.accept()
#         self.send(text_data=json.dumps({'message': 'WebSocket connected!'}))
#
#     def disconnect(self, close_code):
#         pass
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         self.send(text_data=json.dumps({'message': f'You sent: {message}'}))
#
#     def your_message_handler_name(self, event):
#         message = event['message']
#         # Process the message and send it to the client via self.send()
#         self.send(text_data=json.dumps({'message': message}))