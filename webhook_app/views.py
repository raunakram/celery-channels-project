# your_app/views.py
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def s3_notifications(request):
    return render(request, 's3_notification.html')

@csrf_exempt    
def connection_view(request):
    if request.method == 'POST':
        aws_access_key_id = request.POST.get('aws_access_key_id')
        aws_secret_access_key = request.POST.get('aws_secret_access_key')
        region_name = request.POST.get('region_name')
        # return render(request, 's3_notification.html')
        return redirect("/s3_notifications/")
    else:
        return render(request, 'connection_form.html')
        
