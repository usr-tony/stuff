import pandas as pd
import numpy as np
from time import time
import spacy
import sqlite3
import vaex
import os
import bs4
import re

start_time = time()
chunksize = 1000


def keywords(cut_off_days=30):
    time_cutoff = time() - (60 * 60 * 24 * cut_off_days)
    with sqlite3.connect("seek/jobs.db") as con:
        (total,) = con.execute("select count(job_id) from details").fetchone()
    tokenize_words(total, time_cutoff)
    words = vaex.open("seek/words_chunk_*.parquet")
    idf = calc_idf(total, words)
    words, words2id = reduce_size(idf, words)
    idf.export("seek/idf.parquet")
    words.export("seek/words-sm.parquet")
    words2id.export("seek/words2id.parquet")
    remove_intermediate_files()


def tokenize_words(total, time_cutoff):
    rows = pd.read_sql(
        f"""SELECT details.* FROM details
        JOIN jobs ON jobs.id = details.job_id
        where jobs.time > {time_cutoff}""",
        chunksize=chunksize,
        con="sqlite:///seek/jobs.db",
    )
    for i, row in enumerate(rows):
        print(
            "progress:",
            round(i * chunksize / total * 100, 2),
            "%",
            "time elapsed:",
            round(time() - start_time),
            "     ",
            end="\r",
        )
        dfs = row.apply(count_words, axis=1).to_numpy()
        (
            pd.concat(dfs)
            .reset_index()
            .to_parquet(f"seek/words_chunk_{i}.parquet")
        )


def count_words(row, model=spacy.load("en_core_web_sm", exclude=["ner", "parser"])):
    job_id, details = row
    if not type(details) == str:
        details = details.decode("utf-8")

    text = bs4.BeautifulSoup(details, "lxml").text.lower()
    new_words = []
    for w in model(text):
        if w.is_alpha and w.pos_ in ["NOUN", "ADJ"]:
            new_words.append(w.lemma_)

    words_df = (
        pd.DataFrame({"word": new_words})
        .groupby("word")
        .size()
        .to_frame(name="count")
    )

    words_df["id"] = job_id
    return words_df


def calc_idf(total, df):
    gr = df.groupby("word").agg({"count": "count"})
    gr["count"] = np.log(total / gr["count"])
    return gr


def reduce_size(idf, df):
    # aggregates and reduces the size of the chunks produced by tokenize_words
    df["id"] = df["id"].astype("int32")
    df["count"] = df["count"].astype("int16")
    words2id = idf.drop(columns="count")
    words2id["word_id"] = np.arange(len(words2id), dtype=np.int32)
    words = df.join(words2id, on="word", rprefix="r_")
    return words.drop(columns=["r_word", "word"]), words2id


def remove_intermediate_files():
    for file_name in os.listdir("seek"):
        if re.match(r"words_chunk_\d{1,4}\.parquet", file_name):
            os.remove(f"seek/{file_name}")
