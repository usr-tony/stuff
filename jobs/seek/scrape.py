import requests
from bs4 import BeautifulSoup
from time import time, sleep
import subprocess
import json
import re
import pandas as pd
import sqlite3


def scrape():
    with sqlite3.connect('seek/jobs.db') as con:
        try:
            job_id, = con.execute('select max(id) from jobs').fetchone()
        except:
            job_id = input('enter a job id, for example https://seek.com.au/job/[job id]: ')

    consec_errors = 0
    jobs_collected = 0
    while True:
        job_id += 1
        try:
            extract_page(job_id)
            consec_errors = 0
            jobs_collected += 1 
        except Exception as e:
            print(job_id, e, type(e))
            consec_errors += 1

        print(f'{jobs_collected=}', end='\r')
        if consec_errors > 100:
            return print(f'{jobs_collected=}')

    
def extract_page(job_id):
    res = requests.get(f'https://www.seek.com.au/job/{job_id}')
    raw = (BeautifulSoup(res.text, 'lxml')
        .select_one('script[data-automation="server-state"]')
        .string)
    start = 'window.SEEK_REDUX_DATA ='
    end = r';\s+window.SEEK_APP_CONFIG ='
    start_index = raw.index(start) + len(start)
    end_index = re.search(end, raw).start()
    object = raw[start_index: end_index]
    process = subprocess.run(['node', './seek/parse.js', f'({object})'], stdout=subprocess.PIPE)
    data = json.loads(process.stdout)['jobdetails']['result']
    out_df = pd.DataFrame([generate_output(data, job_id)])
    to_local_db(out_df.drop(columns=['details']), 'jobs')
    to_local_db(out_df[['id', 'details']], 'details')
    print(out_df)


def generate_output(job, id):
    return {
        'id': id,
        'title': job['title'],
        'company': job['advertiser']['description'],
        'nation': job['locationHierarchy']['nation'],
        'state': job['locationHierarchy']['state'],
        'city': job['jobLocation'],
        'area': job['jobArea'],
        'suburb': job['locationHierarchy']['suburb'],
        'sector_id': job.get('jobClassificationId') or job['classification']['id'],
        'sector': job.get('jobClassification') or job['classification']['description'], 
        'industry_id': job.get('jobSubClassificationId') or job['subClassification']['id'],
        'industry': job.get('jobSubClassification') or job['subClassification']['description'],   
        'work_type': job['workType'],
        'details': job['jobAdDetails'],
        'time': time()
    }

def to_local_db(df, table='jobs'):
    return df.to_sql(table, con='sqlite:///seek/jobs.db', index=False, if_exists='append')
