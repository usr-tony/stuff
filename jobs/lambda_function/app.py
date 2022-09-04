
import json
import boto3
import io
import pandas as pd
from datetime import timedelta


def get_jobs():
    s3 = boto3.client('s3')
    f = io.BytesIO()
    s3.download_fileobj(Fileobj=f, Key='jobs.parquet', Bucket='jobs--001')
    f.seek(0)
    return pd.read_parquet(f)


def handler(event, context=None):
    params = json.loads(event['body'])
    status_code = 200
    body = get_data(params)
    if not body:
        status_code = 400
        body = 'invalid request parameters'

    return {
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(body),
        'statusCode': status_code,
    }

def get_data(params):
    if params.get('by') in ['sector', 'state', 'company']:
        return grouped_data(params)
    elif params.get('period'):
        return periodic_data(params)


def grouped_data(params):
    group = params.get('by')
    dict_item_results = (get_jobs()
        .groupby(group)['id']
        .count()
        .sort_values(ascending=False)
        .iloc[: 25]
        .to_dict()
        .items()
    )
    return [list(e) for e in dict_item_results]


def periodic_data(params):
    jobs = get_jobs()
    convert_period = {
        'day': seconds(1),
        'week': seconds(7)
    }
    freq = convert_period[params['period']]
    try:
        for key, value in params['filters'].items():
            jobs = jobs[jobs[key] == value]
    except:
        pass

    interval_index = pd.interval_range(
        start=jobs['time'].iloc[-1] - seconds(30),  
        periods=seconds(30) // freq + 1,
        freq=freq,
        closed='right'
    )
    out = pd.cut(jobs['time'], interval_index)
    counts = out.groupby(out).count()
    return list(zip(
        interval_index.left,
        counts.to_numpy().tolist()
    ))

def seconds(days=1):
    return timedelta(days=days).total_seconds()