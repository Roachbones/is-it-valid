# Is it valid?

Twitter bot that posts yes/no polls asking "Is it \[valid|problematic\] to \[transitive verb\] \[noun\]?"

The words are pulled from `wikt.words`, which is an archive of Wiktionary processed by [wiktextract](https://github.com/tatuylonen/wiktextract). The chosen words must also be relatively common, which is determined using `words/count_1w.txt` from http://norvig.com/ngrams/.
