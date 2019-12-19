import json
import os
import boto3
import requests
from read_ingestion_bucket import run_process
from send_to_queue import send_to_queue

def lambda_handler(event, context):
   lambdaName = "Ingest Combine JSON: "
   business_layer_endpoint = os.getenv("BUSINESS_LAYER_ENDPOINT")
   error_queue = os.getenv("ERROR_QUEUE_URL")
   ingestion_output_queue = os.getenv("INGESTION_OUTPUT_QUEUE")
   try:
      post_json = run_process()
      request_response = requests.post(business_layer_endpoint, json.dumps(post_json))
      print('Response: ' + str(request_response))
      print(request_response.text, "TEXT")
      print(request_response.content, "CONTENT")
      print(request_response.status_code, "STATUS CODE")
      output_message = send_to_queue(ingestion_output_queue, str(request_response.content))
      print(output_message)
   except Exception as error:
      errorMessage = lambdaName + " Problem with call to Business Layer " + str(error)
      send_to_queue(error_queue, errorMessage)
      print(errorMessage)
      print('Response: ' + str(request_response))
      print(request_response.content, "CONTENT")
      print(request_response.text, "TEXT")
      print(request_response.status_code, "STATUS CODE")
      return errorMessage