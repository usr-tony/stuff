#! /Users/tony/miniconda3/envs/jobs/bin/python
from seek.scrape import scrape
from time import sleep
from datetime import datetime, timedelta
import gzip
import shutil
import boto3
import os


SLEEP_SECONDS = timedelta(hours=6).seconds
AWS_BUCKET_NAME = 'jobs--001'
SEEK_DB_PATH = './seek/jobs.db'


def main():
    last_uploaded = datetime.now()
    while True:
        scrape()
        if datetime.now() - last_uploaded > timedelta(days=1):
            last_uploaded = datetime.now()
            upload_s3()

        ptime('uploaded to s3, sleeping')
        sleep(SLEEP_SECONDS)


def upload_s3(file_name=SEEK_DB_PATH):
    compressed_file = compress_file(file_name)
    ptime(f'uploading {compressed_file} to s3')
    boto3.client('s3').upload_file(compressed_file, AWS_BUCKET_NAME, compressed_file)
    os.remove(compressed_file)


def compress_file(file_name=SEEK_DB_PATH):
    compressed_file = f'{file_name}.gz'
    ptime(f'creating compressed file ->', compressed_file)
    with gzip.open(compressed_file, 'wb') as fout:
        with open(file_name, 'rb') as fin:
            shutil.copyfileobj(fin, fout)
    
    return compressed_file


def ptime(*msgs):
    print(datetime.now().isoformat(), *msgs)


if __name__ == '__main__':
    main()
        
