import boto3
from datetime import datetime, timedelta
import pytz
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve values from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION')

@shared_task
def monitor_s3():
    def get_s3_client():
        return boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def list_buckets():
        # Get S3 client
        s3_client = get_s3_client()

        # List all buckets
        response = s3_client.list_buckets()

        # Extract and return the bucket names
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        return bucket_names

    def check_new_file_uploaded(bucket_name):
        s3_client = get_s3_client()

        one_minute_ago = datetime.now(pytz.timezone('Asia/Kolkata')) - timedelta(minutes=1)  # Use appropriate timezone

        response = s3_client.list_objects_v2(Bucket=bucket_name)

        for obj in response.get('Contents', []):
            last_modified = obj['LastModified']
            
            if last_modified >= one_minute_ago:
                print(f"New file uploaded in bucket '{bucket_name}': {obj['Key']} at {last_modified}")
                message = f"New file uploaded in bucket '{bucket_name}': {obj['Key']} at {last_modified}"
                send_s3_notification(message)
                return True
            message = f"No new file uploaded in bucket '{bucket_name}' within the last minute."
        # print(f"No new file uploaded in bucket '{bucket_name}' within the last minute.")
            send_s3_notification(message=message)

        return False
    

    def send_s3_notification(message):
        channel_layer = get_channel_layer()
        try:
            async_to_sync(channel_layer.group_send)(
                "s3_notifications",
                {
                    "type": "send_notification",
                    "message": message,
                }
            )
            print("Message sent to group: s3_notifications")
        except Exception as e:
            print(f"Error sending message to group: {e}")



    buckets = list_buckets()
    print("Buckets available:", buckets)


    for bucket_name in buckets:
        check_new_file_uploaded(bucket_name)
