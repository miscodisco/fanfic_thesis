from pathlib import Path

import pandas as pd
import spacy
import textdescriptives as td
from tqdm import tqdm

from utils import *


def main():
    # checking spacy is downloaded to allow for textdescriptives to work
    spacy.load("en_core_web_lg")

    # # load data
    print("[INFO]: loading data")
    fics = read_jsonl("temp2.ndjson")

    # make into dataframe
    print("[INFO]: turning into dataframe")
    df = pd.DataFrame(fics)

    # # subset for testing
    # # df = pd.read_csv("subset.csv")

    # remove duplicates
    df = df.drop_duplicates(subset="work_id")

    # count words, white-space tokenization
    print("[INFO]: counting words and getting snippets")
    word_count = []
    snippets = []

    for text in tqdm(list(df["text"]), total=df.shape[0]):
        clean_text = text.replace("\n", " ")
        tokenized_text = clean_text.split(" ")
        tokenized_text = [token for token in tokenized_text if token != ""]
        fic_length = len(tokenized_text)
        word_count.append(fic_length)

        snip_start, snip_end = get_snip_range(fic_length)
        # snip_start = 100
        # snip_end = 600
        snippets.append(" ".join(tokenized_text[snip_start:snip_end]))

    df["word_count"] = word_count
    df["snippet"] = snippets

    # remove short fics
    df = df.loc[df["word_count"] > 600]

    # make a column with the fandom label
    print("[INFO]: creating fandom label")
    df["fandom_label"] = df.apply(lambda row: get_label(row["fandom"]), axis=1)

    no_fit = df.loc[df["fandom_label"] == "no fit"]
    no_fit.to_csv("no_fit.csv", index=False)

    df.to_csv("all_snippets_full.csv", index=False)

    # get text descriptives
    print("[INFO]: getting quality metrics")
    metrics = td.extract_metrics(text=list(df['snippet']), spacy_model='en_core_web_lg', metrics=['quality'])

    df['passed_qual_check'] = list(metrics['passed_quality_check'])

    # save full df
    df.to_csv("all_snippets_full.csv", index=False)

    # create df with the snippet and meta-data, without the whole text
    meta = df[
        [
            "url",
            "work_id",
            "title",
            "author",
            "published",
            "chapters",
            "kudos",
            "bookmarks",
            "comments",
            "hits",
            "fandom",
            "relationship",
            "character",
            "freeform",
            "rating",
            "words",
            "word_count",
            "fandom_label",
            "snippet",  
            'passed_qual_check'
        ]
    ]

    meta.to_csv("all_snippets_meta.csv", index=False)
    
    print("[INFO]: saving snippets in individual .txt files in corresponding folders")
    for i, snippet in tqdm(enumerate(list(df["snippet"])), total = df.shape[0]):
        # make the out dir the fandom label for the current snippet 
        out_dir = f"all_texts/{list(df['fandom_label'])[i]}/"
        Path(out_dir).mkdir(exist_ok=True)
        # make the filename the work_id 
        with open(f"{out_dir}{list(df['work_id'])[i]}.txt", "w") as f:
            f.write(snippet)


if __name__ == "__main__":
    main()
