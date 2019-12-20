import json
import boto3
import os
import random
import glob
import requests
from boto3 import client
from botocore.vendored.requests.api import request

bucket = os.getenv('INGEST_ZONE_BUCKET')
COUNTER = os.getenv('COUNTER')

def list_files():
    conn = client('s3')
    file_list = []
    counter = 0
    try:
        for key in conn.list_objects(Bucket=bucket)['Contents']:
            if counter <= int(COUNTER):
                file_name=str(key['Key'])
                print(file_name)
                file_list.append(file_name)
                counter += 1
                print(counter)
    except Exception as error:
        print("Error when listing files" + str(error))
        raise Exception
    return file_list

def read_file(filename):
    s3 = boto3.resource("s3")
    try:
        content_object = s3.Object(bucket, filename)
        json_content = content_object.get()['Body'].read().decode('utf-8')
    except Exception as error:
        print("Error when reading files" + error)
        raise Exception
    return json_content

def run_process():
    concatenate_json=[]
    files=list_files()
    try:
        for file in files:
            json_output=read_file(file)
            concatenate_json.append(json.loads(json_output))
        print(concatenate_json)
        output_json = {}
        output_json['batch_data'] = concatenate_json
    except Exception as error:
        print("Error running process" + error)
        raise Exception
    return output_json