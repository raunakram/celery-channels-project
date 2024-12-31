# your_app/views.py
from django.shortcuts import render

def s3_notifications(request):
    return render(request, 's3_notification.html')
