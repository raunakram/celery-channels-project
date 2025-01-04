from django.urls import path
from .views import s3_notifications, connection_view, index

urlpatterns = [
    path('s3_notifications/', s3_notifications, name='s3_notifications'),
    path('connect-s3/', connection_view, name='connection_view'),
    path('rollerbar-check/', index, name='index-view'),
]