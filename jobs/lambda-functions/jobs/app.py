import json
import pandas as pd
from datetime import timedelta

workdir = '/var/task/'


def get_jobs():
    return pd.read_parquet(workdir + 'jobs.parquet')


def handler(event, context=None):
    params = json.loads(event['body'])
    status_code = 200
    body = get_data(params)
    if not body:
        status_code = 401
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
    results = (get_jobs()
               .groupby(params['by'])['id']
               .count()
               .sort_values(ascending=False)
               .iloc[: 25]
               .to_dict()
               )
    return [[k, results[k]] for k in results]


def days2seconds(days=1):
    return timedelta(days=days).total_seconds()


convert_period = {
    'day': days2seconds(1),
    'week': days2seconds(7),
    'month': days2seconds(30),
}


def periodic_data(params):
    jobs = get_jobs()
    try:
        for key, value in params['filters'].items():
            jobs = jobs[jobs[key] == value]
    except:...

    freq = convert_period[params['period']]
    interval_index = pd.interval_range(
        start=jobs['time'].iloc[0],
        periods=total_duration(jobs) // freq + 1,
        freq=freq,
        closed='right'
    )
    out = pd.cut(jobs['time'], interval_index)
    counts = out.groupby(out).count()
    return list(zip(
        interval_index.left,
        counts.to_numpy().tolist()
    ))


def total_duration(df):
    return df['time'].iloc[-1] - df['time'].iloc[0]
