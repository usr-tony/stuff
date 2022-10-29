import pandas as pd
import json

workdir = '/var/task/'

def handler(event, context=None):
    body = json.loads(event['body'])
    words, words2id, idf, jobs = get_files()
    for key in body:
        jobs = jobs[jobs[key] == body[key]]
    ids = jobs['id']
    id_filter = ids.to_frame().set_index('id')
    filtered_words = words.merge(id_filter, on='id', how='inner').drop(columns='id')
    freq = filtered_words.groupby('word_id').agg({'count': 'sum'})
    freq = freq.merge(words2id, on='word_id')
    freq = freq.set_index('word')['count']
    idf = idf.set_index('word')['count']
    tf_idf = (freq * idf).dropna()
    body = (tf_idf
        .sort_values(ascending=False)[:50]
        .to_frame()
        .reset_index()
        .to_numpy()
        .tolist())
    return {
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'statusCode': 200, 
        'body': json.dumps(body)
    }


def get_files():
    filenames = ['words-sm.parquet', 'words2id.parquet', 'idf.parquet',  'jobs.parquet']
    return [pd.read_parquet(workdir + name) for name in filenames]
    