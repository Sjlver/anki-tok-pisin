#!/usr/bin/env python3

"""Finds a good example sentence for a word."""

import math
import re
import sys

def example_sentence(word, sentences, words, bigrams):
    # First, filter the corpus to those sentences containing the word
    sentences = [s for s in sentences if word in s]

    # Sort these by score
    sentences.sort(key=sentence_score(word, words, bigrams), reverse=True)

    return sentences[:3]

def sentence_score(word, words, bigrams):
    def sentence_score_for_word(sentence):
        likelihood_score = sentence_likelihood(sentence, words, bigrams)
        length_score = sentence_length_score(sentence)
        syntax_score = sentence_syntax_score(sentence)

        return likelihood_score * length_score * syntax_score

    return sentence_score_for_word

def sentence_likelihood(sentence, words, bigrams):
    """Computes a likelihood for the given sentence, based on its words and bigrams."""
    sentence = ['</s>'] + re.findall(r'[a-zA-Z]+', sentence) + ['</s>']
    word_ls = []
    bigram_ls = []

    for w in sentence[1:-1]:
        l = max(1,
                words.get(w, 0),
                words.get(w.lower(), 0))
        word_ls.append(math.log(l))
    
    for w1, w2 in zip(sentence, sentence[1:]):
        l = max(1,
                bigrams.get((w1, w2), 0),
                bigrams.get((w1.lower(), w2), 0),
                bigrams.get((w1, w2.lower()), 0),
                bigrams.get((w1.lower(), w2.lower()), 0))
        bigram_ls.append(math.log(l))
    
    return (0.2 * sum(word_ls) / len(word_ls) +
            0.8 * sum(bigram_ls) / len(bigram_ls))

def sentence_length_score(sentence):
    return math.pow(math.log(len(sentence)), -0.7)

def sentence_syntax_score(sentence):
    result = 1.0
    if not re.match(r'^[A-Z].*\.$', sentence):
        result *= 0.5
    return result

with open('corpus/bible/tpi-sentences.txt') as f:
    sentences = [s.strip() for s in f]

with open('corpus/bible/tpi-words.txt') as f:
    words = {}
    for line in f:
        c, w = line.split()
        words[w] = int(c)

with open('corpus/bible/tpi-bigrams.txt') as f:
    bigrams = {}
    for line in f:
        c, w1, w2 = line.split()
        bigrams[(w1, w2)] = int(c)

word = sys.argv[1]

for s in example_sentence(word, sentences, words, bigrams):
    print(s)
