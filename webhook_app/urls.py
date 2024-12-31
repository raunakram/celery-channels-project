from django.urls import path
from .views import s3_notifications

urlpatterns = [
    path('s3_notifications/', s3_notifications, name='s3_notifications'),
]