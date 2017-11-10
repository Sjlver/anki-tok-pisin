#!/usr/bin/env python3

"""Finds a good example sentence for a word."""

import math
import re
import sys

def example_sentence(word, corpus, bigrams):
    # First, filter the corpus to those sentences containing the word
    sentences = [s for s in corpus if word in s]

    # Sort these by score
    sentences.sort(key=sentence_score(word, bigrams), reverse=True)

    return sentences[:3]

def sentence_score(word, bigrams):
    def sentence_score_for_word(sentence):
        likelihood_score = sentence_likelihood(sentence, bigrams)
        length_score = sentence_length_score(sentence)

        return likelihood_score * length_score

    return sentence_score_for_word

def sentence_likelihood(sentence, bigrams):
    """Computes a likelihood for the given sentence, based on its bigrams."""
    sentence = ['</s>'] + re.findall(r'[a-zA-Z]+', sentence) + ['</s>']
    ls = []

    for w1, w2 in zip(sentence, sentence[1:]):
        l = max(1,
                bigrams.get((w1, w2), 0),
                bigrams.get((w1.lower(), w2), 0),
                bigrams.get((w1, w2.lower()), 0),
                bigrams.get((w1.lower(), w2.lower()), 0))
        ls.append(math.log(l))
    
    return sum(ls) / len(ls)

def sentence_length_score(sentence):
    length = sum(len(w) for w in sentence)
    return 1.0 / math.log(length)


with open('corpus/corpus.txt') as f:
    corpus = list(f)

with open('corpus/bigrams.txt') as f:
    bigrams = {}
    for line in f:
        w1, w2, c = line.split()
        bigrams[(w1, w2)] = int(c)

word = sys.argv[1]

for s in example_sentence(word, corpus, bigrams):
    print(s)
