# Function to send data to queue
import boto3
import os
from botocore.exceptions import ClientError

sqs_client = boto3.client('sqs')

def send_outcomes_to_queue(queue_url, data):
    try:
        msg = sqs_client.send_message(QueueUrl=queue_url, MessageBody=data)
    except ClientError as e:
        print("Error in sending to queue: " + e)
        return None
    return msg

def send_to_error_queue(queue_url, errorMessage):
    try:
        queue_url = os.getenv("ERROR_QUEUE_URL")
        msg = sqs_client.send_message(QueueUrl=queue_url, MessageBody=errorMessage)
    except ClientError as e:
        print("Error in sending to queue: " + e)
        return None
    return msg