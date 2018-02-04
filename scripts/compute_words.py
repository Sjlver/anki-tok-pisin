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

def read_sentences_from_corpus(corpus_file):
    """Read sentences from a corpus file"""
    with open(corpus_file) as f:
        sentences = []
        for paragraph in f:
            if paragraph.startswith('#'): continue
            for paragraph_sentence in re.findall(SENTENCE_RE, paragraph):
                if is_well_formed_sentence(paragraph_sentence):
                    sentences.append(clean_sentence(paragraph_sentence))
    return sentences

def clean_sentence(sentence):
    """Remove extra white space from `sentence`."""
    return re.sub(r'\s+', ' ', sentence)

def is_well_formed_sentence(sentence):
    """Checks the sentence for problems such as unmatched parentheses."""
    # TODO: Don't care for the moment.
    return True


def extract_words(sentences):
    all_words = []
    for sentence in sentences:
        words = ['<s>'] + WORD_ONLY_RE.findall(sentence) + ['</s>']
        for word in words:
            all_words.append(word)
    return all_words

def count_words(sentences):
    all_words = extract_words(sentences)
    words = {}
    for w in all_words:
        words[w] = words.get(w, 0) + 1
    del words['<s>']
    del words['</s>']
    return words

def count_bigrams(sentences):
    all_words = extract_words(sentences)
    bigrams = {}
    for b in zip(all_words, all_words[1:]):
        bigrams[b] = bigrams.get(b, 0) + 1
    del bigrams[('</s>', '<s>')]
    return bigrams

def main(args):
    corpus_file, words_file, bigrams_file, sentences_file = args

    sentences = read_sentences_from_corpus(corpus_file)
    words = count_words(sentences)
    bigrams = count_bigrams(sentences)

    with open(words_file, 'w') as f:
        for w, c in sorted(words.items(), key=lambda i: (-i[1], i[0])):
            f.write("{}\t{}\n".format(c, w))

    with open(bigrams_file, 'w') as f:
        for (w1, w2), c in sorted(bigrams.items(), key=lambda i: (-i[1], i[0])):
            f.write("{}\t{}\t{}\n".format(c, w1, w2))

    with open(sentences_file, 'w') as f:
        for s in sentences:
            f.write("{}\n".format(s))

if __name__ == '__main__':
    main(sys.argv[1:])
