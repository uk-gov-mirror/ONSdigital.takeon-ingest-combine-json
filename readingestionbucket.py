import json
import boto3
import os
import random
import glob
import requests
from boto3 import client
from botocore.vendored.requests.api import request


bucket = os.getenv('INGEST_ZONE_BUCKET')

def list_files():
 conn = client('s3')
 file_list = []
 counter = 0
 for key in conn.list_objects(Bucket=bucket)['Contents']:
  if counter <= 50:
   file_name=str(key['Key'])
   print(file_name)
   file_list.append(file_name)
   counter += 1
   print(counter)
  
 return file_list

def read_file(filename):
 s3 = boto3.resource("s3")
 content_object= s3.Object(bucket, filename)
 json_content = content_object.get()['Body'].read().decode('utf-8')
 
 return json_content

def combine_data(json):
 final_dict = {}
 responses = []
 final_dict['reference'] = json["reference"]
 final_dict['period'] = json["period"]
 final_dict['survey'] = json["survey"]
 for k,v in json["responses"].items():
     conc_dict = {}
     conc_dict['questioncode'] = k
     conc_dict['response'] = v
     conc_dict['instance'] = 0
     responses.append(conc_dict)
 final_dict['responses'] = responses


 return final_dict
 
def run_process():
 concatinate_json=[]
 files=list_files()
 for file in files:
  json_output=read_file(file)
  concatinate_json.append(combine_data(json.loads(json_output)))

 print(concatinate_json)

  
