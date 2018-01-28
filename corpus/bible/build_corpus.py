#!/usr/bin/env python3

"""Creates a corpus file from a set of text files."""

import fileinput
import re
import sys

AT_LEAST_ONE_WORD = re.compile(r'[a-zA-Z]{4,}')

# Read input and split in sentences to create corpus.
lines = []
for line in fileinput.input(sys.argv[1:]):
    lines.append(line)

all_text = "".join(lines)

# Remove any characters that aren't letters, numbers, spaces or simple punctuation.
all_text = re.sub(r'''[^A-Za-z0-9.,;:?!… \n-]''', ' ', all_text, flags=re.MULTILINE)

# Remove tokens that have no letter in them. In other words, punctuation must be
# attached to a word for it to be preserved.
old_all_text = None
while all_text != old_all_text:
    old_all_text = all_text
    all_text = re.sub(r'( |^)[^A-Za-z\s]+( |$)', r'\1\2', all_text, flags=re.MULTILINE)

# Collapse multiple spaces and remove single new lines
all_text = re.sub(r'\s*\n\s*\n\s*', r'\n\n', all_text, flags=re.MULTILINE)
all_text = re.sub(r'(\S)\n(\S)', r'\1 \2', all_text, flags=re.MULTILINE)
all_text = re.sub(r'\s* \s*', ' ', all_text, flags=re.MULTILINE)

sentences = re.findall(r'.*?(?:\n\n|\. |\? |! )', all_text)
sentences = [s.strip() for s in sentences]
sentences = [s for s in sentences if AT_LEAST_ONE_WORD.search(s)]
with open('corpus.txt', 'w') as f:
    for sentence in sorted(set(sentences)):
        f.write(sentence + "\n")

# Count words and bigrams
all_words = []
for sentence in sentences:
    sentence = re.sub(r'[^a-z]', ' ', sentence.lower())
    words = ['<s>'] + sentence.split() + ['</s>']
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

with open('words.txt', 'w') as f:
    for w, c in sorted(words.items(), key=lambda i: (-i[1], i[0])):
        f.write("{} {}\n".format(w, c))

with open('bigrams.txt', 'w') as f:
    for (w1, w2), c in sorted(bigrams.items(), key=lambda i: (-i[1], i[0])):
        f.write("{} {} {}\n".format(w1, w2, c))
