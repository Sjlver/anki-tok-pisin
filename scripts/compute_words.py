#!/usr/bin/env python3

"""Computes word and bigram statistics on a corpus"""

import re
import sys

# A sentence starts with a capital letter, contains at least three
# words, and ends with a sentence-ending punctuation string. This
# is a bit picky... but better few nice sentences than bad ones.
ALL_CHARS_RE = 'r[A-Za-z0-9,.:!?()“”‘’#/*†‡§ \n_–—-]'
WORD_RE = r'[“‘]?[A-Za-z0-9–—-]+[,:)”’]?'
START_OF_SENTENCE_RE = r'[“‘]?[A-Z0-9]'
END_OF_SENTENCE_RE = r'[.!?][”’]?'
SENTENCE_RE = re.compile(
        START_OF_SENTENCE_RE + WORD_RE +
        r'(?:\s+' + WORD_RE + '){2,}' +
        END_OF_SENTENCE_RE
        )
WORD_ONLY_RE = re.compile(r'[A-Za-z0-9](?:[A-Za-z0-9–—-]*[A-Za-z0-9]|)')

# Read sentences from a corpus file
corpus_file = sys.argv[1]
words_file = sys.argv[2]
bigrams_file = sys.argv[3]
sentences_file = sys.argv[4]
with open(corpus_file) as f:
    sentences = []
    for paragraph in f:
        if paragraph.startswith('#'): continue
        for paragraph_sentence in re.findall(SENTENCE_RE, paragraph):
            sentences.append(re.sub(r'\s+', ' ', paragraph_sentence))


# Count words and bigrams
all_words = []
for sentence in sentences:
    words = ['<s>'] + WORD_ONLY_RE.findall(sentence) + ['</s>']
    for word in words:
        all_words.append(word)

words = {}
bigrams = {}

for w in all_words:
    words[w] = words.get(w, 0) + 1
for b in zip(all_words, all_words[1:]):
    bigrams[b] = bigrams.get(b, 0) + 1

del words['<s>']
del words['</s>']
del bigrams[('</s>', '<s>')]

with open(words_file, 'w') as f:
    for w, c in sorted(words.items(), key=lambda i: (-i[1], i[0])):
        f.write("{} {}\n".format(w, c))

with open(bigrams_file, 'w') as f:
    for (w1, w2), c in sorted(bigrams.items(), key=lambda i: (-i[1], i[0])):
        f.write("{} {} {}\n".format(w1, w2, c))

with open(sentences_file, 'w') as f:
    for s in sentences:
        f.write("{}\n".format(s))
