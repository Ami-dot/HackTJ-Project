# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
from botocore.exceptions import ClientError
import os

AWS_KEY = 'AKIAQR3YZ4H235UYSAPF'
AWS_SECRET = 'ETA2VMZO0u337b1cVgyi05+mZkzLJADmAyzZil0N'

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    # s3_client = boto3.client('s3')
    session = boto3.Session()
    s3_client = session.client('s3',aws_access_key_id=AWS_KEY,
            region_name = 'us-east-1',
            aws_secret_access_key=AWS_SECRET)

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def detect_text(photo, bucket):

    session = boto3.Session()
    client = session.client('rekognition',aws_access_key_id=AWS_KEY,
                region_name = 'us-east-1',
                aws_secret_access_key=AWS_SECRET)

    response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})

    textDetections = response['TextDetections']
    print('Detected text\n----------')
    for text in textDetections:
        textininput = text['DetectedText']
        print(text['DetectedText'])
    return len(textDetections)

def main():
    bucket = 'swiftstudy'
    photo = 'bionotes.png'
    upload_file(photo, bucket)
    text_count = detect_text(photo, bucket)
    print(str(text_count))

if __name__ == "__main__":
    main()
