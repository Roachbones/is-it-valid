# Is it valid?

Mastodon bot that posts yes/no polls asking "Is it \[valid|problematic\] to \[transitive verb\] \[noun\]?"

Word lists are mined from `wikt.words` (not tracked), which is an archive of Wiktionary processed by [wiktextract](https://github.com/tatuylonen/wiktextract). The chosen words must also be relatively common, which is determined using `words/count_1w.txt` from http://norvig.com/ngrams/. The word lists are manually edited afterwards.

This used to be a Twitter bot, but I moved it to Mastodon.