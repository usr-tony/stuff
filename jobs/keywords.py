import pandas as pd
import numpy as np
from time import time
import spacy
import sqlite3

con = 'sqlite:///seek/jobs.db'

start_time = time()

# def calculate_idf():
#     total_jobs = pd.read_sql('select count(id) from jobs', con=con,)['count(id)'][0]
#     results = pd.Series(dtype=int)
#     df_gen = pd.read_sql('select * from words', con=con, chunksize=chunksize)
#     for counter, df in enumerate(df_gen):
#         word_counts = df.groupby('word').count()['id']
#         results = results.add(word_counts, fill_value=0)
#         print_progress(counter + 1)
    
#     idf = np.log(total_jobs / results)
#     return idf


def tokenize_words():
    model = spacy.load('en_core_web_sm', exclude=['tok2vec', 'ner', 'parser'])
    print(model.pipeline)
    con = sqlite3.connect('./seek/jobs.db')
    total, = con.execute('select count(id) from details').fetchone()
    counter = chunk_counter = 0
    dfs = []
    for id, details in con.execute('select * from details'):
        if not type(details) == str:
            details = details.decode('utf-8')

        new_words = [w.lemma_ for w in model(details.lower()) if w.is_alpha]
        words_df = pd.DataFrame({'word': new_words})
        words_df['count'] = 1
        words_df = words_df.groupby('word').sum()
        words_df['id'] = id
        dfs.append(words_df)
        counter += 1
        print('progress:', round(counter / total * 100, 2), '%', 'time elapsed:', time() - start_time, '     ', end='\r')
        if len(dfs) > 10 ** 4 or counter == total - 1:
            chunk_counter += 1
            df = pd.concat(dfs)
            df.reset_index().to_parquet(f'./seek/words_chunk_{chunk_counter}.parquet')
            dfs = []


if __name__ == '__main__':
    tokenize_words()
