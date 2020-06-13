"""
This script uses the word lists generated by word_filter.py to
generate questions for the bot to ask.
"""

import random
import inflect
import curated
p = inflect.engine() #this is just for p.a(noun)

basic_innocence_levels = ["valid","problematic"]
bonus_innocence_levels = [
    "homophobic","bigoted","transphobic",
    "cursed","sexy","blessed","anti-gamer",
    "safe","okay","cool","legal","against the rules"
]

noun_tuples = [] #like [("product","s"),("tables","p"),("food","u")...]

noun_tuples.extend((i, "singular") for i in curated.singular_nouns)
noun_tuples.extend((i, "plural") for i in curated.plural_nouns)
noun_tuples.extend((i, "uncountable") for i in curated.uncountable_nouns)
noun_tuples.extend((i, "articled") for i in curated.articled_nouns)

def pick_innocence():
    if random.random() < 0.8:
        return random.choice(basic_innocence_levels)
    else:
        return random.choice(bonus_innocence_levels)
def pick_noun():
    noun, plurality = random.choice(noun_tuples)
    if plurality == "singular":
        return random.choice((
            p.a(noun),
            "the " + noun,
            "your " + noun
        )) #every, any
    if plurality == "plural" or plurality == "uncountable":
        # there are tons of plural nouns. give the others a better chance
        if random.random() < 0.5:
            return pick_noun()
        if random.random() < 0.70:
            return noun
        else:
            return random.choice(("the", "your")) + " " + noun
            #plural: all, a few, several, many
            #uncountable: all, a little, a lot of
    if plurality == "articled":
        return noun      

def generate():
    s = "Is it {} to {} {}".format(
        pick_innocence(),
        random.choice(curated.verbs),
        pick_noun() 
    )
    if random.random() < 0.98:
        s = s + "?"
    else:
        s = s + " " + random.choice((
            "every day",
            "once a week",
            "in the middle of the night",
            "when nobody is looking"
        )) + "?"
    return s

if __name__ == "__main__":
    while True:
        input(generate())
