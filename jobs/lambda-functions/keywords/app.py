import pandas as pd
import json
import vaex

workdir = '/var/task/'

def handler(event, context=None):
    body = json.loads(event['body'])
    words, words2id, jobs = vaex_read_files()
    for key in body:
        jobs = jobs[jobs[key] == body[key]]
    
    freq = (words
        .join(jobs[['id']], on='id', how='inner')
        .groupby('word_id')
        .agg({'count': 'sum'})
        .join(words2id, on='word_id')
        .to_pandas_df()
        .set_index('word')
        ['count']
    )
    idf = pd.read_parquet(workdir + 'idf.parquet').set_index('word')['count']
    df_idf = ((idf * freq)
        .dropna()
        .sort_values(ascending=False)
        [: 50]
        .to_frame()
        .reset_index()
        .to_numpy()
        .tolist()
    )
    return {
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'statusCode': 200, 
        'body': json.dumps(df_idf)
    }


def vaex_read_files():
    filenames = ['words-sm.parquet', 'words2id.parquet',  'jobs.parquet']
    return [vaex.open(workdir + name) for name in filenames]
    