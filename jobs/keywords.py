import enum
import pandas as pd
import numpy as np
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from time import time
from datetime import timedelta


con = 'sqlite:///seek/jobs.db'

ProgressBar().register()
start_time = time()
total_words = 183000000
chunksize = 999999

def calculate_idf():
    total_jobs = pd.read_sql('select count(id) from jobs', con=con,)['count(id)'][0]
    results = pd.Series(dtype=int)
    df_gen = pd.read_sql('select * from words', con=con, chunksize=chunksize)
    for counter, df in enumerate(df_gen):
        word_counts = df.groupby('word').count()['id']
        results = results.add(word_counts, fill_value=0)
        print_progress(counter + 1)
    
    idf = np.log(total_jobs / results)
    return idf


def condense_words():
    pd.read_sql('select * from words', con=con, chunksize=chunksize):
        


def print_progress(counter):
    print('progress:', counter * chunksize / total_words * 100)
    print('time elapsed:', timedelta(seconds=time() - start_time))



def words_to_db(df):
    import spacy

    model = spacy.load('en_core_web_trf', exclude=['ner', 'parser', 'transformer'])
    counter = 0
    total = len(df)
    for id, details in df.to_numpy():
        try:
            details = details.decode('utf-8')
        except:
            pass

        doc = model(details.lower())
        words = {}
        for token in doc:
            if not token.is_alpha:
                continue

            try:
                words[token.lemma_] += 1
            except:
                words[token.lemma_] = 1

        words_df = pd.DataFrame([(w, words[w]) for w in words], columns=['word', 'count'])
        words_df['id'] = id
        #words_df.to_sql('words', con='sqlite:///seek/jobs.db', if_exists='append', index=False)
        counter += 1
        print('progress:', round(counter / total * 100, 2), '%  ', end='\r')


def inverse_document_frequency(bag):
    result = len(bag) / bag.groupby('word').count()
    return np.log(result)


def document_frequency(small_bag):
    return small_bag.groupby('word').sum()


if __name__ == '__main__':
    main()
