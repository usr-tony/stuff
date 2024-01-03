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
UPLOAD_PERIOD: timedelta = timedelta(days=1)


def main():
    last_uploaded = datetime.now()
    while True:
        scrape()
        if datetime.now() - last_uploaded > UPLOAD_PERIOD:
            last_uploaded = datetime.now()
            upload_s3()

        ptime('sleeping')
        sleep(SLEEP_SECONDS)


def upload_s3(file_name=SEEK_DB_PATH):
    compress_file(file_name)
    compressed_file = get_compressed_path(file_name)
    ptime(f'uploading {compressed_file} to s3')
    boto3.client('s3').upload_file(compressed_file, AWS_BUCKET_NAME, compressed_file)
    os.remove(compressed_file)
    ptime('uploaded to s3')


def compress_file(file_name=SEEK_DB_PATH):
    compressed_file_path = get_compressed_path(file_name)
    ptime(f'creating compressed file ->', compressed_file_path)
    with gzip.open(compressed_file_path, 'wb') as fout:
        with open(file_name, 'rb') as fin:
            shutil.copyfileobj(fin, fout)


def ptime(*msgs: str) -> None:
    print(datetime.now().isoformat(), *msgs)


def get_compressed_path(file_name: str=SEEK_DB_PATH) -> str:
    return f'{file_name}.gz'


if __name__ == '__main__':
    main()
        
