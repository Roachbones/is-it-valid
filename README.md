# Is it valid?

Twitter bot that posts yes/no polls asking "Is it \[valid|problematic\] to \[transitive verb\] \[noun\]?"

The words are pulled from `wikt.words` (not tracked), which is an archive of Wiktionary processed by [wiktextract](https://github.com/tatuylonen/wiktextract). The chosen words must also be relatively common, which is determined using `words/count_1w.txt` from http://norvig.com/ngrams/.

## Working around the lack of API support for polls

As of August 2019, the Twitter API does not support poll creation. So, unfortunately, the bot must use Selenium WebDriver to control a Firefox window to tweet a poll.

There was an OAuth-spoofing method used by [JeuDuDicoBot](https://github.com/WhiteFangs/JeuDuDicoBot/) and several others in order to tweet polls, but [it does not work now](https://github.com/WhiteFangs/JeuDuDicoBot/issues/1). If new application keys are discovered that allow this method, or if the Twitter API adds poll support, please let me know. You could even just give me a spare set of poll-creating API keys if you have them.
