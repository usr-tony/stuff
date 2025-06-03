from time import time
import json
import pandas as pd
import boto3
from os import path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import traceback


file_dir = path.dirname(__file__)
CON = f'sqlite:///{file_dir}/jobs.db'
POOL_SIZE = 900
JOBS_PER_FUNCTION = 30 # must be a factor of pool_size
NODE = '~/.nvm/versions/node/v23.5.0/bin/node'

pd.options.display.width = 200

def scrape():
    largest_id = find_largest_job_id()
    for i in range(1):
        jobs_list = use_node_scraper(largest_id + POOL_SIZE * i)
        if not jobs_list:
            print(f'no jobs found for ids between {largest_id + POOL_SIZE * i} and {largest_id + POOL_SIZE * (i + 1)}')
            continue

        jobs = pd.concat(jobs_list)
        write2db(jobs)


def find_largest_job_id():
    rows = pd.read_sql(
        'select max(id) from jobs',
        con=CON
    )
    if len(rows):
        return int(rows.iloc[0, 0])
    
    return input('enter a job id e.g. (seek.com.au/job/{job_id}')


def use_node_scraper(largest_id):
    job_id = largest_id + 1
    processes = POOL_SIZE // JOBS_PER_FUNCTION
    job_ids = np.split(
        np.arange(job_id, POOL_SIZE + job_id),
        processes
    )
    with ThreadPoolExecutor(max_workers=processes) as executor:
        results = executor.map(node_scraper, job_ids)

    return [j for jobs in results for j in jobs]


def node_scraper(job_ids=[61373164, 61373165], debug=True):
    if type(job_ids) != list:
        job_ids = job_ids.tolist()

    res = (boto3
        .Session()
        .client('lambda')
        .invoke(
            FunctionName='seek-scraper-node',
            Payload=json.dumps({'job_ids': job_ids})
        ))
    
    data = json.loads(res['Payload'].read())
    if debug:
        print(json.dumps(data))

    results = []
    for job, job_id in zip(data, job_ids):
        if not job:
            continue
        
        try:
            results.append(generate_output(job, job_id))
        except Exception:
            print(job_id, job)
            traceback.print_exc()

    return results


def write2db(jobs):
    print(jobs.drop(columns=['details', 'id', 'time', 'sector_id', 'industry_id']))
    to_local_db(jobs.drop(columns=['details']), 'jobs')
    to_local_db(
        jobs[['id', 'details']].rename(columns={'id': 'job_id'}),
        'details'
    )


def generate_output(data, id):
    job = data['jobdetails']['result']['job']
    classification = job['tracking']['classificationInfo'] 
    location = job['tracking']['locationInfo']
    try:
        salary = job['salary']['label']
    except (ValueError, TypeError):
        salary = None

    return pd.DataFrame([dict(
        id=id,
        title=job['title'],
        company=job['advertiser']['name'],
        salary=salary,
        city=location['location'],
        area=get_area(job),
        sector_id=classification['classificationId'],
        sector=classification['classification'],
        industry_id=classification['subClassificationId'],
        industry=classification['subClassification'],
        work_type=job['workTypes']['label'],
        details=job['content'],
        time=time(),
        posted=get_posted(job)
    )])


def get_posted(job: dict):
    listed_at = job['listedAt']
    return listed_at.get('shortLabel') or listed_at.get('label')
    

def get_area(job: dict):
    location = job['tracking']['locationInfo']
    try:
        return location['area'] or job['location']['label']
    except KeyError:
        return None

    
def to_local_db(df, table='jobs'):
    return df.to_sql(table, con=CON, index=False, if_exists='append')



