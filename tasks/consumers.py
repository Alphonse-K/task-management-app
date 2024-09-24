from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f'notifications_{self.user.id}'
        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()  # Close connection for unauthenticated users

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle messages from WebSocket if needed
        pass

    async def send_notification(self, event):
        
        notification = event['notification']
        print(f"Sending notification: {notification}")  # Debug log
        await self.send(text_data=json.dumps(notification))


