"""
Toots questions generated by question_generator.py.
"""

import json
from time import sleep
from mastodon import Mastodon
from question_generator import generate

SECONDS_BETWEEN_POSTS = 25 * 60 * 60 #every 25 hours

mastodon = Mastodon(access_token="token")

poll = mastodon.make_poll(
    options=["yes","no"],
    expires_in=SECONDS_BETWEEN_POSTS
)

def post_question():
    status = generate()
    print("Posting question: '{}'... ".format(status), end="")
    mastodon.status_post(status, poll=poll)
    print("done! :3")

while True and 0:
    post_question()
    sleep(SECONDS_BETWEEN_TWEETS)
