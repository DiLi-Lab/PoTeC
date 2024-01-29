#!/usr/bin/env python3
"""
#TODO
Call: #TODO
"""
import argparse
import json
import os
from pathlib import Path

import pandas as pd


def aoi2word(aoi: int, word_limits: list) -> int:
    """
    Creates mapping between aoi and word index in text. Word_limits is a list of two lists, containing the first and
    the last aoi of a word. Checks whether aoi is in a word interval and returns the word index in the text.
    Returns a negative index if it is between two words.
    """
    for index, (word_start_aoi, word_end_aoi) in enumerate(zip(word_limits[0], word_limits[1])):
        if word_start_aoi <= aoi <= word_end_aoi:
            return index + 1
        # if the aoi is smaller than the start of the word and the end of the word but apparently also not in the word
        # before that word we know it is not in a word
        if aoi < word_start_aoi:
            return - index - 1


def char_index_to_word_index(limits_file: Path, output_file: Path) -> None:
    with open(limits_file, 'r') as limits_json:
        limits = json.load(limits_json)

    texts = ["b0", "b1", "b2", "b3", "b4", "b5", "p0", "p1", "p2", "p3", "p4", "p5"]

    item_ids = []
    word_indices = []
    aois = []

    for text_id in texts:
        text_limits = limits[text_id]
        max_aoi = (text_limits[1][-1])  # end of the last word, i.e. maximal aoi number
        iter_aois = range(1, max_aoi + 1)  # all aois

        # iterate over all aois (i.e. all char ids) in one text
        for aoi in iter_aois:
            # word index in text
            word_index = aoi2word(aoi, text_limits)

            word_indices.append(word_index)
            item_ids.append(text_id)
            aois.append(aoi)

    data_dict = {
        'text_id': item_ids,
        'word_index_in_text': word_indices,
        'char_index_in_text': aois
    }

    data_df = pd.DataFrame(data_dict)
    data_df.to_csv(output_file, sep='\t', index=False)


def main() -> int:
    repo_root = Path(__file__).parent.parent

    word_limits = repo_root / 'preprocessing_scripts/word_limits.json'
    output_file = repo_root / 'preprocessing_scripts/aoi_to_word.tsv'

    char_index_to_word_index(
        word_limits,
        output_file
    )

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

