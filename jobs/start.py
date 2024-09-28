from seek.scrape import scrape
from time import sleep
from datetime import datetime, timedelta
import gzip
import shutil
import boto3
import os
from pathlib import Path


SLEEP_SECONDS = timedelta(hours=6).seconds
AWS_BUCKET_NAME = 'jobs--001'
SEEK_DB_PATH = './seek/jobs.db'
UPLOAD_PERIOD: timedelta = timedelta(days=3)


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
    compressed_file_path = compress_file(file_name)
    ptime(f'uploading {compressed_file_path} to s3')
    boto3.client('s3').upload_file(
        compressed_file_path, 
        AWS_BUCKET_NAME, 
        Path(compressed_file_path).parts[-1],
        ExtraArgs=dict(
            StorageClass='STANDARD' # infrequent access tier
        )
    )
    os.remove(compressed_file_path)
    ptime('uploaded to s3')


def compress_file(file_name=SEEK_DB_PATH):
    compressed_file_path = f'{file_name}.gz'
    ptime(f'creating compressed file ->', compressed_file_path)
    with gzip.open(compressed_file_path, 'wb') as fout:
        with open(file_name, 'rb') as fin:
            shutil.copyfileobj(fin, fout)

    return compressed_file_path


def ptime(*msgs: str) -> None:
    print(datetime.now().isoformat(), *msgs)


if __name__ == '__main__':
    main()
        
