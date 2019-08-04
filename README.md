# Is it valid?

Twitter bot that posts yes/no polls asking "Is it \[valid|problematic\] to \[transitive verb\] \[noun\]?"

The words are pulled from `wikt.words` (not tracked), which is an archive of Wiktionary processed by [wiktextract](https://github.com/tatuylonen/wiktextract). The chosen words must also be relatively common, which is determined using `words/count_1w.txt` from http://norvig.com/ngrams/.

## Working around the lack of API support for polls

The bot posts polls using a weird workaround because the Twitter API doesn't actually let you create polls. It took me a while to figure out this workaround, so I'll explain it here in case you want to do something similar.

The creation of a poll-tweet has two steps:

1. A request to create the poll "card", (to `https://caps.twitter.com/v2/cards/create.json`), returning the `card_uri` associated with the newly created poll. This doesn't actually publish the poll anywhere, it just makes it available to publish with the second step.
2. A request to publish a tweet with that poll attached to it (to `https://api.twitter.com/1.1/statuses/update.json`).

As of August 2019, Twitter API does not let you do the first step, but it lets you do the second, as long as you have the `card_uri` associated with the poll that you want to post.

So, the solution used here was to repeatedly do the first step in a browser while recording the returned `card_uri`s to use later. This was done by using a browser extension to block requests to `https://api.twitter.com/1.1/statuses/update.json` from being sent, and then repeatedly clicking the Tweet button. The requests sent to `https://caps.twitter.com/v2/cards/create.json` were exported to `poll_hacking/requests.har` and then processed by `poll_hacking/card_lister.py`.

This approach works because we know what kind of polls we want to post before we post them, because all of this bot's poll cards are identical; a yes/no poll with a duration of one day. If you want to dynamically post polls with answers that you can't predict ahead of time, then this approach won't work.
