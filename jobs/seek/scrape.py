import requests
from bs4 import BeautifulSoup
from time import time, sleep
import subprocess
import json
import re
import pandas as pd
import sqlite3
import base64
import boto3
from os import path


pd.options.display.max_columns = 99
file_dir = path.dirname(__file__)


def scrape():
    with sqlite3.connect(file_dir + '/jobs.db') as con:
        try:
            job_id, = con.execute('select max(id) from jobs').fetchone()
        except:
            job_id = input(
                'enter a job id, for example https://seek.com.au/job/[job id]: ')

    consec_errors = 0
    jobs_collected = 0
    while True:
        job_id += 1
        try:
            html = get_html(job_id, True)
            out_df = extract_page(job_id, html)
            to_local_db(out_df.drop(columns=['details']), 'jobs')
            to_local_db(out_df[['id', 'details']], 'details')
            print(out_df)
            consec_errors = 0
            jobs_collected += 1
        except Exception as e:
            print(job_id, e, type(e))
            consec_errors += 1

        print(f'{jobs_collected=}')
        if consec_errors > 100:
            return print(f'{jobs_collected=}')


def get_html(job_id, from_lambda=False):
    if not from_lambda:
        return requests.get(f'https://www.seek.com.au/job/{job_id}').text

    return html_from_lambda(job_id)


def extract_page(job_id, html):
    raw = (BeautifulSoup(html, 'lxml')
           .select_one('script[data-automation="server-state"]')
           .string)
    start = 'window.SEEK_REDUX_DATA ='
    end = r';\s+window.SEEK_APP_CONFIG ='
    start_index = raw.index(start) + len(start)
    end_index = re.search(end, raw).start()
    object = raw[start_index: end_index]
    process = subprocess.run(
        ['node', file_dir + '/parse.js', f'({object})'], stdout=subprocess.PIPE)
    parsed_object = json.loads(process.stdout)
    # print(json.dumps(parsed_object, indent=4)) # uncomment to activate detailed logging
    job = parsed_object['jobdetails']['result']['job']
    return pd.DataFrame([generate_output(job, job_id)])


def generate_output(job, id):
    classification = job['tracking']['classificationInfo']
    location = job['tracking']['locationInfo']
    return {
        'id': id,
        'title': job['title'],
        'company': job['advertiser']['name'],
        'nation': None,
        'state': None,
        'city': location['location'],
        'area': location['area'],
        'suburb': None,
        'sector_id': classification['classificationId'],
        'sector': classification['classification'],
        'industry_id': classification['subClassificationId'],
        'industry': classification['subClassification'],
        'work_type': job['workTypes']['label'],
        'details': job['content'],
        'time': time(),
        'posted': job['listedAt']['shortLabel']
    }


def to_local_db(df, table='jobs'):
    return df.to_sql(table, con=f'sqlite:///{file_dir}/jobs.db', index=False, if_exists='append')


def html_from_lambda(job_id):
    data = json.loads(
        boto3
        .Session(profile_name='personal')
        .client('lambda')
        .invoke(
            FunctionName='seek-scraper',
            Payload=json.dumps({'job_id': job_id}).encode()
        )['Payload']
        .read()
        .decode('utf-8')
    )
    return base64.b64decode(data).decode('utf-8')


if __name__ == '__main__':
    print(extract_page(58887346))
