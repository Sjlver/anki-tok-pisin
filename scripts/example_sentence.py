#!/usr/bin/env python3

"""Finds a good example sentence for a word."""

import argparse
import json
import math
import re

def example_sentence(word, sentences, words, bigrams):
    # First, filter the corpus to those sentences containing the word
    sentences = [s for s in sentences if
        re.search(r'\b' + re.escape(word) + r'\b', s, re.IGNORECASE)]

    # Find the best
    if not sentences:
        return None
    return max(sentences, key=sentence_score(word, words, bigrams))

def sentence_score(word, words, bigrams):
    def sentence_score_for_word(sentence):
        likelihood_score = sentence_likelihood(sentence, words, bigrams)
        length_score = sentence_length_score(sentence)

        return likelihood_score * length_score

    return sentence_score_for_word

# The likelyhood of a sentence depends on the sentence alone => Compute it only
# once.
likelyhood_cache = {}

def sentence_likelihood(sentence, words, bigrams):
    """Computes a likelihood for the given sentence, based on its words and bigrams."""
    cached = likelyhood_cache.get(sentence, None)
    if cached is not None:
        return cached

    sentence_words = ['</s>'] + re.findall(r'[a-zA-Z]+', sentence.lower()) + ['</s>']
    word_ls = []
    bigram_ls = []

    for w in sentence_words[1:-1]:
        l = max(1, words.get(w, 0))
        word_ls.append(math.log(l))
    
    for w1, w2 in zip(sentence_words[:-1], sentence_words[1:]):
        l = max(1, bigrams.get((w1, w2), 0))
        bigram_ls.append(math.log(l))
    
    likelyhood = (0.2 * sum(word_ls) +
                  0.8 * sum(bigram_ls))
    likelyhood_cache[sentence] = likelyhood
    return likelyhood

def sentence_length_score(sentence):
    return math.pow(len(sentence), -1.2)

def process_note(note, sentences, words, bigrams):
    assert len(note["fields"]) >= 2, "Note must have word fields."

    if len(note["fields"]) > 2 and note["fields"][2]:
        # Already has an example sentence. Leave it alone.
        return note
    elif len(note["fields"]) == 2:
        note["fields"].append("")

    word = note["fields"][0]
    example = example_sentence(word, sentences, words, bigrams)
    if example:
        note["fields"][2] = example
    return note


def main():
    parser = argparse.ArgumentParser(description="Compute example sentences.")
    parser.add_argument("--sentences-file", help="File to load sentences from.",
            type=argparse.FileType('r'),
            default="corpus/corpuscrawler/tpi-sentences.txt")
    parser.add_argument("--words-file", help="File to load words from.",
            type=argparse.FileType('r'),
            default="corpus/corpuscrawler/tpi-words.txt")
    parser.add_argument("--bigrams-file", help="File to load bigrams from.",
            type=argparse.FileType('r'),
            default="corpus/corpuscrawler/tpi-bigrams.txt")
    parser.add_argument("--word", help="Word for which to compute an example sentence.")
    parser.add_argument("--anki", help="CrowdAnki file to process",
            type=argparse.FileType('r'))
    parser.add_argument("--output", help="CrowdAnki file to write",
            type=argparse.FileType('w'))

    args = parser.parse_args()

    if ((not args.word and not args.anki) or
            (args.word and args.anki)):
        raise ValueError("Specify exactly one of --word or --anki")
    if args.anki and not args.output:
        raise ValueError("--anki requires --output")

    sentences = list(set([s.strip() for s in args.sentences_file]))

    words = {}
    for line in args.words_file:
        c, w = line.split()
        w = w.lower()
        words[w] = words.get(w, 0) + int(c)

    bigrams = {}
    for line in args.bigrams_file:
        c, w1, w2 = line.split()
        w1, w2 = w1.lower(), w2.lower()
        bigrams[(w1, w2)] = bigrams.get((w1, w2), 0) + int(c)

    if (args.word):
        print(example_sentence(args.word, sentences, words, bigrams))
    else:
        anki = json.load(args.anki)
        notes = [process_note(note, sentences, words, bigrams) for note in anki["notes"]]
        anki["notes"] = notes
        json.dump(anki, args.output, sort_keys=True, indent=4)

if __name__ == '__main__':
    main()
