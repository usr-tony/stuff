from seek import scrape
from time import sleep
from datetime import datetime
import boto3
import io
import pandas as pd
from config import local as local_db
from time import time


def main():
    while True:
        scrape.scrape()
        cache_to_s3()
        print(datetime.now().isoformat())
        sleep(60 * 60 * 12)


def cache_to_s3():
    jobs = pd.read_sql(f'''
        SELECT id, title, company, nation, state, sector, industry, time FROM jobs
    ''', con=local_db)
    f = io.BytesIO()
    jobs.to_parquet(f, index=None)
    f.seek(0)
    s3 = boto3.Session(profile_name='personal').client('s3')
    s3.upload_fileobj(f, Key='jobs.parquet', Bucket='jobs--001')
    print('cached')


if __name__ == '__main__':
    main()
        
