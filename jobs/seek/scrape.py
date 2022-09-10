#!/Users/tony/miniconda3/envs/jobs/bin/python
import requests
from bs4 import BeautifulSoup
from time import sleep, time
from random import random
from . import database
from .headers import headers
import subprocess
import json
import re
import sqlite3
import pandas as pd


def scrape(job_id=None): # this id may not be relevant
    con, cur = database.create_connection()
    if not job_id:
        job_id = find_largest_job_id(cur)

    consec_errors = 0
    while True:
        job_id += 1
        try:
            Page(job_id, cur)
            consec_errors = 0
        except Exception as e:
            print(job_id, e)
            consec_errors += 1
        
        if consec_errors > 500:
            break
            
        sleep(random()/10)
        con.commit()
    
    con.commit()
    con.close()


def remove_old_rows(cur):
    # deletes jobs scraped more than 30 days ago
    time_threshold = int(time()) - 60 * 60 * 24 * 30
    cur.execute('DELETE FROM jobs WHERE time < ' + str(time_threshold))


def Page(job_id, remote_cur=None):
    base_url = 'https://www.seek.com.au/job/'
    url = base_url + str(job_id)
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
    sector = job.get('jobClassification')
    if not sector:
        sector = job['classification']['description']

    sector_id = job.get('jobClassificationId')
    if not sector_id:
        sector_id = job['classification']['id']

    industry = job.get('jobSubClassification')
    if not industry:
        industry = job['subClassification']['description']

    industry_id = job.get('jobSubClassificationId')
    if not industry_id:
        industry_id = job['subClassification']['id']
 
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
    if remote_cur:
        remote_cur.execute(
            'INSERT INTO jobs VALUES (' + ','.join(['%s'] * 15) + ')',
            [output[o] for o in output]
        )

    out_df = pd.DataFrame([output])
    to_local_db(out_df.drop(columns=['details']), 'jobs')
    to_local_db(out_df[['id', 'details']], 'details')
    print(job_id, output['title'], output['company'], output['area'], output['city'])
        

def to_local_db(df, table='jobs'):
    return df.to_sql(table, con=database.local, index=False, if_exists='append')


def find_largest_job_id(cur):
    cur.execute('SELECT MAX(id) AS id FROM jobs')
    job_id = cur.fetchone()['id']
    if not job_id:
        job_id = input('enter job id to begin search from from seek.com.au/job/[job id]: ')
        job_id = int(job_id)

    return job_id
