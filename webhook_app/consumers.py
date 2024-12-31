# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class S3NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "s3_notifications"

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

    async def send_notification(self, event):
        print(f"Checking event-------: {event}")
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))

