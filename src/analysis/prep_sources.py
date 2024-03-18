from pathlib import Path
import os

def main():

    files = [file for file in os.listdir("raw_sources") if file.endswith(".txt")]

    for file in files:
        # keep track of progress 
        print(file)

        # open file
        with open("raw_sources/"+file, "r") as f:
            temp = f.read()

        # white-space tokenize
        tokenized = temp.replace("\n", "").split(" ")
        print(len(tokenized))

        # create out folder 
        out_dir = f"source_texts/{Path(file).stem}_source/"
        Path(out_dir).mkdir(exist_ok=True)

        # for every 5,000 words, extract 500 and save them in a separate .txt file
        for i in range(0, len(tokenized), 5000):
            # get the words
            snippet = tokenized[i + 100 : i + 600]

            # turn them from list to string
            snippet_text = ' '.join(snippet)

            with open(f"{out_dir}{i}_source.txt", "w") as f:
                f.write(snippet_text)
            

if __name__ == "__main__":
    main()