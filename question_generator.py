"""
This script uses the word lists generated by word_filter.py to
generate questions for the bot to ask.
"""

import random
import inflect
p = inflect.engine() #this is just for p.a(noun)

basic_innocence_levels = ["valid","problematic"]
bonus_innocence_levels = [
    "homophobic","bigoted","transphobic",
    "cursed","sexy","blessed","anti-gamer",
    "safe","okay","cool","legal","against the rules"
]

with open("words/generated_transitive_verbs.txt", "r", encoding="utf-8") as file:
    verbs = file.read().split("\n")

noun_tuples = [] #like [("product","s"),("tables","p"),("craft","u")...]
with open("words/generated_singular_nouns.txt","r",encoding="utf-8") as file:
    noun_tuples.extend((i, "s") for i in file.read().split("\n"))
with open("words/generated_plural_nouns.txt","r",encoding="utf-8") as file:
    noun_tuples.extend((i, "p") for i in file.read().split("\n"))
with open("words/generated_uncountable_nouns.txt","r",encoding="utf-8") as file:
    noun_tuples.extend((i, "u") for i in file.read().split("\n"))

def pick_innocence():
    if random.random() < 0.8:
        return random.choice(basic_innocence_levels)
    else:
        return random.choice(bonus_innocence_levels)
def pick_noun():
    noun, flavor = random.choice(noun_tuples)
    if flavor == "u":
        if random.random() < 0.8:
            return noun
        else:
            return "the " + noun
    if flavor == "s":
        return random.choice((
            p.a(noun),
            "the " + noun,
            "my " + noun
        ))
    if flavor == "p":
        if random.random() < 0.5:
            return noun
        else:
            return random.choice((
                "the " + noun,
                "my " + noun
            ))

def generate():
    s = "Is it {} to {} {}?"
    s = s.format(
        pick_innocence(),
        random.choice(verbs),
        pick_noun() 
    )
    return s

if __name__ == "__main__":
    while True:
        input(generate())
