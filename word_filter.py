"""
This script reads through wikt.words and words/count_1w.txt to
make the word lists used to generate sentences.
Each word can have multiple consecutive entries in wikt.words,
each corresponding to a different part of speech.
Furthermore, each entry can have multiple definitions.
Both the entries and the definitions are listed in decreasing order
of how often the word is used in that sense (like a dictionary).
When determining if a word is eligible to go into one of our lists,
we only consider the first definition of the first part of speech,
therefore only considering the most common use of the word.
Otherwise, we get weird inclusions, like "safety" as a verb.
"""

import json

MINIMUM_WORD_LENGTH = 4

with open("words/blacklist.txt","r",encoding="utf-8") as file:
    blacklist = file.read().split("\n")

COMMONNESS_LIMIT = 3375348 #see words/count_1w.txt
common_words = []
with open("words/count_1w.txt","r",encoding="utf-8") as file:
    for line in file:
        entry = line.split()
        if int(entry[1]) < COMMONNESS_LIMIT:
            break
        common_words.append(entry[0])

#these lists will be mutually exclusive
transitive_verbs = []
singular_nouns = []
plural_nouns = []
uncountable_nouns = []

def wiktwords(): #generator, yields all wiktextract entries in order
    with open("words/wikt.words","r",encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)

def get_entry(word): #slow; just for debugging
    for entry in wiktwords():
        if entry["word"] == word:
            return entry
    return None

#count_1w.txt ignores case, so we get false common words,
#like the plurals "yemen", "greece", and "netherlands".
#filtering out everything that can be a name cuts out too much,
#but let's at least filter out the countries.
countries = [] #lowercase
for entry in wiktwords():
    if (
        entry["pos"] == "name" and
        "senses" in entry and
        "glosses" in entry["senses"][0] and
        "country" in entry["senses"][0]["glosses"][0].lower()
    ):
        countries.append(entry["word"].lower())
blacklist.extend(countries)

last_word = None
for entry in wiktwords():
    if entry["word"] == last_word:
        #we only want to consider the first entry for each word
        continue
    if (
        not "senses" in entry or
        not "tags" in entry["senses"][0] or
        len(entry["word"]) < MINIMUM_WORD_LENGTH
    ):
        last_word = entry["word"]
        continue
    
    if (
        entry["pos"] == "verb" and
        "transitive" in entry["senses"][0]["tags"] and
        entry["word"] in common_words and
        not entry["word"] in blacklist
    ):
        transitive_verbs.append(entry["word"])
    elif entry["pos"] == "noun":
        if (
            "countable" in entry["senses"][0]["tags"] and
            entry["word"] in common_words and
            not entry["word"] in blacklist
        ):
            singular_nouns.append(entry["word"])
        elif (
            "plural" in entry["senses"][0]["tags"] and
            entry["word"] in common_words and
            not entry["word"] in blacklist
        ):
            plural_nouns.append(entry["word"])
        elif (
            "uncountable" in entry["senses"][0]["tags"] and
            entry["word"] in common_words and
            not entry["word"] in blacklist
        ):
            uncountable_nouns.append(entry["word"])
    last_word = entry["word"]
        
print(len(transitive_verbs), "transitive verbs")
print(len(singular_nouns), "singular nouns")
print(len(plural_nouns), "plural nouns")
print(len(uncountable_nouns), "uncountable nouns")

with open("words/generated.json","w",encoding="utf8") as file:
    json.dump(
        {
            "transitive_verbs": transitive_verbs,
            "singular_nouns": singular_nouns,
            "plural_nouns": plural_nouns,
            "uncountable_nouns": uncountable_nouns
        },
        file,
        indent=4
    )

print("done! :3")

def bad_words(): #to lazily check for slurs
    with open("words/bad_words.txt","r",encoding="utf-8") as file:
        bad_words = file.read().split("\n")
    for word in transitive_verbs+singular_nouns+plural_nouns+uncountable_nouns:
        for bad_word in bad_words:
            if bad_word in word:
                print(word, bad_word)
