import json
import os
from readextractbucket import run_process
from writetoqueue import write_to_queue

def lambda_handler(event, context):
   try:
      run_process()
   except:
      queue_url = os.getenv("ERROR_QUEUE_URL")
      print("queue_url: " + queue_url)
      msg = write_to_queue(queue_url, json.dumps("{\"Error\": \"Could not process files\""))
      print(msg)
      return "Error: could not process files"
      


