Anki Deck for Tok Pisin
=======================

This repository contains a semi-automated way to create an Anki deck for
learning *Tok Pisin*.

Tok Pisin is the primary language spoken in Papua New Guinea. It is a trade
language derived from English. The basic vocabulary is small; this deck contains
about 1800 notes. This makes it particularly suitable for learning with Anki.


Overview of Our Approach
------------------------

1.  Obtain a list of words and their translation.

    This project scrapes the dictionary at <http://www.tok-pisin.com/> to
    obtain a basic list of words.

2.  Form cards from these words.

    In this step, we try to smartly group words with multiple translations.
    This is common in Tok Pisin. Our goal is to find a way for users to learn
    the multiple meanings of a word, without confusing users.

3.  Prioritize cards.

    Learning is much easier if the frequently-used and important words are
    learned first. We use word frequency data and manual prioritization to
    create a good card order.

4.  Augment cards with extra information.

    We try to make cards as informative and beautiful as possible. First, we
    obtain a corpus of Tok Pisin from freely available texts. We primarily use
    the Bible, because it contains high-quality text with translation, and
    because it is freely available. From this corpus, we select example
    sentences for our cards, rank them, and add the best example to the card.

    Second, we look up information on English words, to make our cards more
    canonical. For example, we would transform "drive" into "to drive" to make
    it clear to the user that we're looking for the verb, not the noun.


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
