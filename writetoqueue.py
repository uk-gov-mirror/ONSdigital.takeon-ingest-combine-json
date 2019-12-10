# Function to send data to queue
import boto3
# import logging
from botocore.exceptions import ClientError
def write_to_queue(queue_url, msg_body):
    sqs_client = boto3.client('sqs')
    try:
        msg = sqs_client.send_message(QueueUrl=queue_url,
                                      MessageBody=msg_body)
    except ClientError as e:
        print("Error in sending to queue: " + e)
        # logging.error(e)
        return None
    return msg