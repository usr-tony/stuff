from time import time
import json
import pandas as pd
import boto3
from os import path
from concurrent.futures import ThreadPoolExecutor
import numpy as np


file_dir = path.dirname(__file__)
CON = f'sqlite:///{file_dir}/jobs.db'
POOL_SIZE = 900
JOBS_PER_FUNCTION = 30 # must be a factor of pool_size


def scrape():
    largest_id = find_largest_job_id()
    for i in range(20): # tries 900 * 20 job ids after the largest
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

    results = [j for jobs in results for j in jobs]
    return results


def node_scraper(job_ids=[61373164, 61373165], debug=False):
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
        except Exception as e:
            print('start exception:', e, job_ids, res, '\n', data)

    return results


def write2db(jobs):
    print(jobs.iloc[:, 1: 6])
    to_local_db(jobs.drop(columns=['details']), 'jobs')
    to_local_db(
        jobs[['id', 'details']].rename(columns={'id': 'job_id'}),
        'details'
    )


def generate_output(data, id):
    job = data['jobdetails']['result']['job']
    classification = job['tracking']['classificationInfo'] 
    location = job['tracking']['locationInfo']
    area = location['area']
    if not area:
        try:
            area = job['location']['label']
        except:
            pass

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
        area=area,
        sector_id=classification['classificationId'],
        sector=classification['classification'],
        industry_id=classification['subClassificationId'],
        industry=classification['subClassification'],
        work_type=job['workTypes']['label'],
        details=job['content'],
        time=time(),
        posted=job['listedAt']['shortLabel']
    )])


def to_local_db(df, table='jobs'):
    return df.to_sql(table, con=CON, index=False, if_exists='append')



