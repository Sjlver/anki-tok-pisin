#!/usr/bin/env python3

"""Sorts notes by priority and frequency."""

import argparse
import json
import math
import re

def process_note(note, words):
    note_words = [w.lower() for w in note["fields"][0].split()]
    popularity = min(words.get(w, 0) for w in note_words)
    note["fields"][5] = str(popularity)
    return note

def note_sort_key(note):
    priority = 3
    popularity = 0
    if note["tags"]:
        priority = int(note["tags"][0])
    popularity = int(note["fields"][5])
    return (priority, -popularity)

def main():
    parser = argparse.ArgumentParser(description="Order notes by priority and word frequency.")
    parser.add_argument("--words-file", help="File to load words from.",
            type=argparse.FileType('r'),
            default="corpus/corpuscrawler/tpi-words.txt")
    parser.add_argument("--anki", help="CrowdAnki file to process",
            type=argparse.FileType('r'))
    parser.add_argument("--output", help="CrowdAnki file to write",
            type=argparse.FileType('w'))

    args = parser.parse_args()

    if not args.anki:
        raise ValueError("--anki is required")
    if args.anki and not args.output:
        raise ValueError("--anki requires --output")

    words = {}
    for line in args.words_file:
        c, w = line.split()
        w = w.lower()
        words[w] = words.get(w, 0) + int(c)

    anki = json.load(args.anki)
    notes = [process_note(note, words) for note in anki["notes"]]
    notes.sort(key=note_sort_key)
    anki["notes"] = notes
    json.dump(anki, args.output, sort_keys=True, indent=4)

if __name__ == '__main__':
    main()
