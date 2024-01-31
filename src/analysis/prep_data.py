from pathlib import Path

import pandas as pd
import textdescriptives as td 
from tqdm import tqdm

from utils import * 


def main():
    # load data
    print("[INFO]: loading data")
    fics = read_jsonl("temp2.ndjson")

    # make into dataframe 
    print("[INFO]: turning into dataframe")
    df = pd.DataFrame(fics)
    
    # subset for testing 
    # df = pd.read_csv("subset.csv")

    # remove duplicates
    df = df.drop_duplicates(subset="work_id")

    # count words, white-space tokenization
    print("[INFO]: counting words and getting snippets")
    word_count = []
    snippets = []

    for text in tqdm(list(df['text']), total=len(df['work_id'])):
        temp = text.replace("\n", " ").split(" ")
        word_count.append(len(temp))
        snippets.append(' '.join(temp[100:600]))

    df['word_count'] = word_count
    df['snippet'] = snippets

    # remove short fics
    df = df.loc[df['word_count'] > 600]

    # make a column with the fandom label 
    print("[INFO]: creating fandom label")
    df['fandom_label'] = df.apply(lambda row: get_label(row['fandom']), axis=1)

    no_fit = df.loc[df['fandom_label'] == "no fit"]
    no_fit.to_csv("no_fit.csv", index=False)

    # get a sample of the data
    print("[INFO]: getting subset")
    pj_subset = df.loc[df['fandom_label'] == "PJ"].sample(n=1000)
    hp_subset = df.loc[df['fandom_label'] == "HP"].sample(n=1000)
    lotr_subset = df.loc[df['fandom_label'] == "LOTR"].sample(n=1000)

    sample_df = pd.concat([pj_subset, hp_subset, lotr_subset])
    
    sample_df.to_csv("snippets_full.csv", index=False)

    # get text descriptives 
    print("[INFO]: getting quality metrics")
    metrics = td.extract_metrics(text=list(sample_df['snippet']), spacy_model='en_core_web_lg', metrics=['quality'])

    sample_df['passed_qual_check'] = list(metrics['passed_quality_check'])

    # save full df
    sample_df.to_csv("snippets_full.csv", index=False)

    # create df with the snippet and meta-data, without the whole text 
    meta = sample_df[['url', 'work_id', 'title', 'author', 'published', 'chapters',
       'kudos', 'bookmarks', 'comments', 'hits', 'fandom', 'relationship',
       'character', 'freeform', 'rating', 'words', 'word_count', 'fandom_label', 'snippet', 'passed_qual_check']]

    meta.to_csv('snippets_meta.csv', index=False)

    # DECIDE WHETHER FAILS ON THE QUAL CHECK SHOULD BE EXCLUDED 

    print("[INFO]: saving snippets in individual .txt files in corresponding folders")
    for i, snippet in enumerate(list(sample_df['snippet'])):
        # get the corresponding fandom label for the current snippet 
        out_dir = f"texts/{list(sample_df['fandom_label'])[i]}/"
        Path(out_dir).mkdir(exist_ok=True)

        # e.g. texts/PJ/0_fic.txt
        with open(f"{out_dir}{i}_fic.txt", 'w') as f:
            f.write(snippet)

if __name__ == "__main__":
    main()