from __future__ import print_function

import urllib
import boto3
from wand.image import Image

print('Loading function')

def handler(event, context):
    try:
        client = boto3.client('s3')

        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))

        response = client.get_object(Bucket = bucket, Key = key)

        file_path = '/tmp/' + key

        response = client.download_file(bucket, key, file_path)

        image = Image(filename=file_path)

        image.resize(int(240), int(240))

        resize_key = key.replace(".jpg", "_resize.jpg")

        resize_file_path = '/tmp/' + resize_key

        image.format = 'jpg'

        image.save(filename=resize_file_path)

        response = client.upload_file(resize_file_path, "serverlesspro-service-resized-imgs", resize_key)

        print(resize_key + " has been uploaded!")

    except Exception as e:
        print(e)