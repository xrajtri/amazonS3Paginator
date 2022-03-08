import json
import os
import sys
import tempfile
import boto3

def lambda_handler(event, context):
    
    # Fetching the request data
    print("Loading lambda function - s3 pagniator to traverse and find particular file")
    print(event)
    # message_data = event["body"] #Required when lambda function is going to be called from API gateway.
    #data = json.loads(message_data) #Required when lambda function is going to be called from API gateway.
    fileNameToSearch = event["fileNameToSearch"]
    print("File name to search is : {}".format(fileNameToSearch))
    
    # Fetching environment variables values
    BUCKET_NAME = os.environ['BUCKET_NAME']

    # Prepare temporary files
    def get_all_s3_objects(s3, **base_kwargs):
        continuation_token = None
        while True:
            list_kwargs = dict(MaxKeys=1000, **base_kwargs)
            if continuation_token:
                list_kwargs['ContinuationToken'] = continuation_token
            response = s3.list_objects_v2(**list_kwargs)
            yield from response.get('Contents', [])
            if not response.get('IsTruncated'):  # At the end of the list?
                return "noFileFound"
                break
            continuation_token = response.get('NextContinuationToken')
            
    for file in get_all_s3_objects(boto3.client('s3'), Bucket=BUCKET_NAME, Prefix=fileNameToSearch):
        print("File response")
        print(file)
        print(file['Key'])
        if file.get('Key'):
            print("File exists.")
            message = "File exists."
            return{
                "statusCode":200,
                "body":json.dumps(message)
            }