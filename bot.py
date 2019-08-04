"""
This script uses the twitter API to post twitter polls with questions
generated by question_generator.py.
"""

import json
import oauth2
from time import sleep
from urllib.parse import urlencode
from question_generator import generate

with open("secret_keys.txt", "r") as file:
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET = file.read().split("\n")

def oauth_req(url, http_method="POST", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    client = oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=bytes(post_body, "utf-8"), headers=http_headers)
    return content

def get_card_uri():
    """
    The Twitter API doesn't let us create polls,
    but we can attach pre-existing poll cards to our tweets.
    This function grabs one from a big list that was pre-generated with keypress automation,
    and then removes it from that list so we don't reuse it later.
    Hopefully, we can make polls through the API by the time the list runs out.
    """
    with open("poll_hacking/card_uris.txt", "r") as file:
        card_uris = file.read().split("\n")
        assert card_uris != [""], "We ran out of card_uris!"
        card_uri = card_uris.pop()
    with open("poll_hacking/card_uris.txt", "w") as file:
        file.write("\n".join(card_uris))
    return card_uri

def post_question():
    status = generate()
    card_uri = get_card_uri()
    querystring = "?" + urlencode({"status":status, "card_uri":card_uri})
    response = json.loads(oauth_req("https://api.twitter.com/1.1/statuses/update.json" + querystring).decode("utf8"))
    assert not "errors" in response, reponse
    print("Posted question: '{}' with tweet id {} and card_uri {}.".format(response["text"], response["id"], card_uri))

SECONDS_BETWEEN_TWEETS = 23 * 60 * 60 #every 23 hours

while True:
    post_question()
    sleep(SECONDS_BETWEEN_TWEETS)
