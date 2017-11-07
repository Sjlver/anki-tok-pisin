#!/usr/bin/env python3

from bs4 import BeautifulSoup
import csv
import itertools

def extract_words(soup):
    words = []
    for tr in soup.find_all('tr'):
        tds = tr.contents
        if (len(tds) == 2 and
                tds[0].name == 'td' and tds[0].font is not None and
                tds[1].name == 'td' and tds[1].font is not None):
            words.append((tds[0].font.string.strip(), tds[1].font.string.strip()))
                
    return words

def group_words(words):
    """If words appear multiple times, group all occurrences."""

    # First, split any cases where multiple meanings are grouped already
    split_words = []
    for w in words:
        for meaning in w[0].split(', '):
            split_words.append((meaning, w[1]))

    # Then, combine both the original and translated languages
    words = sorted(split_words, key=lambda w: w[0])
    combined = []
    for k, g in itertools.groupby(words, lambda w: w[0]):
        combined.append((k, " | ".join(w[1] for w in g)))

    words = sorted(combined, key=lambda w: w[1])
    combined = []
    for k, g in itertools.groupby(words, lambda w: w[1]):
        combined.append((" | ".join(w[0] for w in g), k))

    return combined


def read_priority():
    """Creates a list of words, roughly sorted by priority."""

    priority = []
    with open('priority/world_english.tsv') as f:
        cr = csv.DictReader(f, delimiter="\t")
        for row in cr:
            priority.append(row['Word'])

    with open('priority/basic_english.txt') as f:
        for line in f:
            priority.append(line.strip())

    # Remove duplicates
    words = set()
    for i in range(len(priority)):
        if priority[i] in words:
            priority[i] = None
        else:
            words.add(priority[i])

    return [w for w in priority if w is not None]


def sorted_by_priority(words, priority):
    ranks = dict(zip(priority, range(len(priority))))

    return sorted(words, key=lambda w: ranks.get(w[1], len(ranks)))


def main(args):
    words = []
    for filename in args:
        with open(filename) as f:
            soup = BeautifulSoup(f, 'html.parser')
            words.extend(extract_words(soup))

    words = group_words(words)

    priority = read_priority()
    words = sorted_by_priority(words, priority)

    with open('dictionary.csv', 'w') as f:
        fw = csv.writer(f)
        fw.writerow(('ID', 'Tok Pisin', 'English'))
        for i, w in enumerate(words):
            fw.writerow((i, w[0], w[1]))


if __name__ == '__main__':
    import sys
    main(sys.argv)
