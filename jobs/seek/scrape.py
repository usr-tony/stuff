import requests
from bs4 import BeautifulSoup
from time import time
import subprocess
import json
import re
import pandas as pd
import base64
import boto3
from os import path
from concurrent.futures import ProcessPoolExecutor


file_dir = path.dirname(__file__)
pool_size = 100


def scrape():
    job_id = find_largest_job_id()
    while jobs_list := scrape_multiple(job_id):
        jobs = pd.concat(jobs_list)
        print(jobs)
        write2db(jobs)
        job_id += pool_size


def find_largest_job_id():
    rows = pd.read_sql(
        'select max(id) from jobs',
        con=f'sqlite:///{file_dir}/jobs.db'
    )
    if len(rows):
        return int(rows.iloc[0, 0])
    else:
        return input('enter a job id e.g. (seek.com.au/job/{job_id}')


def scrape_multiple(starting_job_id):
    with ProcessPoolExecutor(max_workers=10) as executor:
        scraped_results = executor.map(
            scrape_job,
            [starting_job_id + i + 1 for i in range(pool_size)]
        )
    return list(
        filter(lambda x: type(x) == pd.DataFrame, scraped_results)
    )


def write2db(jobs):
    to_local_db(jobs.drop(columns=['details']), 'jobs')
    to_local_db(
        jobs[['id', 'details']].rename(columns={'id': 'job_id'}),
        'details'
    )


def scrape_job(job_id):
    try:
        html = get_html(job_id)
        data = extract_page(html)
        return generate_output(data, job_id)
    except Exception as e:
        return e


def extract_page(html):
    raw = (BeautifulSoup(html, 'lxml')
           .select_one('script[data-automation="server-state"]')
           .string)
    start = 'window.SEEK_REDUX_DATA ='
    end = r';\s+window.SEEK_APP_CONFIG ='
    start_index = raw.index(start) + len(start)
    end_index = re.search(end, raw).start()
    object = raw[start_index: end_index]
    process = subprocess.run(
        ['node', file_dir + '/parse.js', f'({object})'],
        stdout=subprocess.PIPE
    )
    parsed_object = json.loads(process.stdout)
    return parsed_object


def generate_output(data, id):
    job = data['jobdetails']['result']['job']
    classification = job['tracking']['classificationInfo']
    location = job['tracking']['locationInfo']
    return pd.DataFrame([{
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
    }])


def to_local_db(df, table='jobs'):
    return df.to_sql(table, con=f'sqlite:///{file_dir}/jobs.db', index=False, if_exists='append')


def get_html(job_id, from_lamda_proxy=True):
    if not from_lamda_proxy:
        return requests.get(f'https://www.seek.com.au/job/{job_id}').text
        
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
