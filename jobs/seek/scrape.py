import requests
from bs4 import BeautifulSoup
from time import time, sleep
from .headers import headers
import subprocess
import json
import re
import pandas as pd
import sqlite3
import sys
sys.path.append('../')


def scrape(job_id=None): # this id may not be relevant
    if not job_id:
        with sqlite3.connect('seek/jobs.db') as con:
            job_id, = con.execute('select max(id) from jobs').fetchone()


    consec_errors = 0
    while True:
        job_id += 1
        sleep(0.3)
        try:
            Page(job_id)
            consec_errors = 0
        except Exception as e:
            print(job_id, e)
            consec_errors += 1
        
        if consec_errors > 500:
            break


def Page(job_id):
    url = f'https://www.seek.com.au/job/{job_id}'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    tag, = soup.select('script[data-automation="server-state"]')
    raw = tag.string
    start = 'window.SEEK_REDUX_DATA ='
    end = r';\s+window.SEEK_APP_CONFIG ='
    start_index = raw.index(start) + len(start)
    end_index = re.search(end, raw).start()
    object = raw[start_index: end_index]
    process = subprocess.run(['node', './seek/parse.js', f'({object})'], stdout=subprocess.PIPE)
    data = json.loads(process.stdout)
    job = data['jobdetails']['result']
    sector = job.get('jobClassification') or job['classification']['description']
    sector_id = job.get('jobClassificationId') or job['classification']['id']
    industry = job.get('jobSubClassification') or job['subClassification']['description']
    industry_id = job.get('jobSubClassificationId') or job['subClassification']['id']
    output = {
        'id': job_id,
        'title': job['title'],
        'company': job['advertiser']['description'],
        'nation': job['locationHierarchy']['nation'],
        'state': job['locationHierarchy']['state'],
        'city': job['jobLocation'],
        'area': job['jobArea'],
        'suburb': job['locationHierarchy']['suburb'],
        'sector_id': sector_id,
        'sector': sector, 
        'industry_id': industry_id,
        'industry': industry,   
        'work_type': job['workType'],
        'details': job['jobAdDetails'],
        'time': time()
    }

    out_df = pd.DataFrame([output])
    to_local_db(out_df.drop(columns=['details']), 'jobs')
    to_local_db(out_df[['id', 'details']], 'details')
    print(job_id, sector, industry)
        

def to_local_db(df, table='jobs'):
    return df.to_sql(table, con='sqlite:///seek/jobs.db', index=False, if_exists='append')
