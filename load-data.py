#!/usr/bin/env python3
import os
from google.cloud import storage
import configparser

## Get data
config = configparser.ConfigParser()
config.read('config.ini')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sust-dev-01-3ba63a5afe5a.json' ## Change to your local key
#Set up file download parameters from Google Cloud Storage
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print('OK - downloaded: ' + source_blob_name)

download_blob(config['GS_CLOUD']['BUCKET_ID'],config['GS_CLOUD']['FILE_ID'],'data/raw_data.csv')