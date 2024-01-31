import json


def read_jsonl(path: str) -> list[dict]:
    """
    takes an .ndjson file, and return a list of dictionaries 
    where each dictionary corresponds to a line in the file. 
    """
    with open(path, "r") as jsonl_file:
        object = [json.loads(line.strip()) for line in jsonl_file]
    return object



def get_label(fandom_tags) -> str:
    """
    get the fandom label based on the fandom tags on the fic 
    """
    if 'The Lord of the Rings - J. R. R. Tolkien' in fandom_tags or 'Lord of the Rings - J. R. R. Tolkien' in fandom_tags or 'Rings' in fandom_tags:
        return 'LOTR'
    elif 'Percy Jackson and the Olympians - Rick Riordan' in fandom_tags or 'Percy' in fandom_tags:
        return 'PJ'
    elif 'Harry Potter - J. K. Rowling' in fandom_tags or 'Potter' in fandom_tags:
        return 'HP'
    else:
        return 'no fit'


