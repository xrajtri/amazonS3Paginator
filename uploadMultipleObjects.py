import json
import os
import sys
import tempfile
import boto3

def lambda_handler(event, context):
    
    # Fetching the request data
    print("Loading lambda function - s3 pagniator")
    print(event)
    # message_data = event["body"] #Required when lambda function is going to be called from API gateway.
    #data = json.loads(message_data) #Required when lambda function is going to be called from API gateway.
    data = event["fileNameToSearch"]
    print("Data is {}".format(data))
    nosOfObjects = event["nosOfObjects"]
    print("Total nos of objects to be uploaded to S3 is {}".format(nosOfObjects))
    tempData = {
        "fileName":"test",
        "data":"kla;dfhkl;ajdfljasdklf;jalskdjfklasjdfkljasdklfjalskdfjlasjdf;lkajsdfkljasdklfjaslkdfja"
    }
    
    # Fetching environment variables values
    BUCKET_NAME = os.environ['BUCKET_NAME']

    # Prepare temporary files
    s3 = boto3.resource('s3')
    counter = 1
    while counter <= nosOfObjects:
        print("Creating temp file for record number {}".format(counter))
        tempFileName = "test_"+str(counter)+".json"
        path = "/tmp/"+tempFileName
        with open(path,"w") as outfile:
            json.dump(tempData,outfile)
            # Upload nos of files to S3
            print("Uploading record number {}".format(counter))
            s3Response = s3.meta.client.upload_file(path,BUCKET_NAME,tempFileName)
            counter += 1
    
    # Response to be sent as lambda response
    message = "Event data has been processed"
    return{
        "statusCode":200,
        "body":json.dumps(message)
    }