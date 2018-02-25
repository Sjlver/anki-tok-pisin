Anki Deck for Tok Pisin
=======================

An [Anki flash cards deck][deck] to learn Tok Pisin.

**Tok Pisin** is the primary language spoken in **Papua New Guinea.** This deck
contains the vocabulary to get you started as a speaker of Tok Pisin. The deck
contains around 1700 notes consisting of a Tok Pisin word, the English
translation, and an example sentence to illustrate how the word is used.

This deck will get you a long way toward being a speaker of Tok Pisin, because
the language is easy to learn. Tok Pisin started as a trade language derived
from English. Its vocabulary is small: the 1700 words in this deck cover most
words used in day-to-day conversations. The grammar is much easier to learn than
English, too. For example, verbs do not change depending on the tense or the
person. Once you learn a verb on a card, you can use it in any grammatical
situation.

This deck is a collaborative work. Development happens on GitHub at
[Sjlver/anki-tok-pisin][github]. You suggestions, improvements or ideas are most
welcome!

[deck]: https://ankiweb.net/shared/info/1365902313
[github]: https://github.com/Sjlver/anki-tok-pisin


How this deck was created
-------------------------

1.  Obtain a list of words and their translation.

    This project scraped the dictionary at <http://www.tok-pisin.com/> to
    obtain a basic list of words.

2.  Form cards from these words.

    We tried to smartly group words with multiple translations. This is common
    in Tok Pisin. Our goal was to find a way for users to learn the multiple
    meanings of a word, without confusing users.

3.  Prioritize cards.

    Learning is much easier if the frequently-used and important words are
    learned first. We used word frequency data and manual prioritization to
    create a good card order.

4.  Augment cards with extra information.

    We try to make cards as informative and beautiful as possible. First, we
    obtain a corpus of Tok Pisin from freely available texts, using [Google's
    CorpusCrawler][corpuscrawler]. From this corpus, we select example
    sentences for our cards, rank them, and add the best example to the card.

    Second, we look up information on English words, to make our cards more
    canonical. For example, we would transform "drive" into "to drive" to make
    it clear to the user that we're looking for the verb, not the noun.

[corpuscrawler]: https://github.com/googlei18n/corpuscrawler 


Inspiration
-----------

[Natural Language Corpus Data: Beautiful Data](http://norvig.com/ngrams/) \
Beautiful examples on how to use corpora and ngrams to solve various language
related tasks.

[Ultimate Geography Deck](https://github.com/axelboc/anki-ultimate-geography) \
One of the best Anki desks. Managed collaboratively on GitHub. Uses CrowdAnki to
represent decks in JSON format.

[MorphMan plugin for Anki](https://github.com/kaegi/MorphMan) \
Re-orders cards, so that each card introduces just a little new information.

[What works and what doesn't](https://info.maths.ed.ac.uk/assets/files/LandT/what_works_what_doesnt.pdf) \
A study on study techniques.
