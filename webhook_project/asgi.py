# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from webhook_app.consumers import S3NotificationConsumer
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webhook_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            # Route to your consumer
            path('ws/s3_notifications/', S3NotificationConsumer.as_asgi()),
        ])
    ),
})
