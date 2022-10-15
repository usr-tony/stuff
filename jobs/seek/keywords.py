import pandas as pd
import numpy as np
from time import time
import spacy
import sqlite3
import vaex
import os

start_time = time()


def generate_exports():
    with sqlite3.connect('seek/jobs.db') as con:
        total, = con.execute('select count(id) from details').fetchone()
    tokenize_words(total)
    words = vaex.open('seek/words_chunk_*.parquet')
    idf = calc_idf(total, words)
    words, words2id = reduce_size(idf, words)
    idf.export('seek/idf.parquet')
    words.export('seek/words-sm.parquet')
    words2id.export('seek/words2id.parquet')
    os.system("find ./seek -name 'words_chunk_*.parquet' -delete")


def tokenize_words(total):
    model = spacy.load('en_core_web_sm', exclude=['tok2vec', 'ner', 'parser'])
    counter = chunk_counter = 0
    dfs = []
    con = sqlite3.connect('seek/jobs.db')
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
            (pd.concat(dfs)
                .reset_index()
                .to_parquet(f'words_chunk_{chunk_counter}.parquet'))
            dfs = []
    con.close()


def calc_idf(total, df):
    gr = df.groupby('word').agg({'count': 'count'})
    gr['count'] = np.log(total / gr['count'])
    return gr


def reduce_size(idf, df):
    # aggregates and reduces the size of the chunks produced by tokenize_words
    df['id'] = df['id'].astype('int32')
    df['count'] = df['count'].astype('int16')
    words2id = idf.drop(columns='count')
    words2id['word_id'] = np.arange(len(words2id), dtype=np.int32)
    words = df.join(words2id, on='word', rprefix='word_')
    return words.drop(columns=['word_word', 'word']), words2id
