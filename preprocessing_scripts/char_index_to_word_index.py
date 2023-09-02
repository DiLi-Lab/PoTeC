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


def roi2word(roi: int, word_limits: list) -> int:
    """
    Creates mapping between roi and word index in text. Word_limits is a list of two lists, containing the first and
    the last roi of a word. Checks whether roi is in a word interval and returns the word index in the text.
    Returns a negative index if it is between two words.
    """
    for index, (word_start_roi, word_end_roi) in enumerate(zip(word_limits[0], word_limits[1])):
        if word_start_roi <= roi <= word_end_roi:
            return index + 1
        # if the roi is smaller than the start of the word and the end of the word but apparently also not in the word
        # before that word we know it is not in a word
        if roi < word_start_roi:
            return - index - 1


def char_index_to_word_index(limits_file: str, output_file: str) -> None:
    with open(limits_file, 'r') as limits_json:
        limits = json.load(limits_json)

    texts = ["b0", "b1", "b2", "b3", "b4", "b5", "p0", "p1", "p2", "p3", "p4", "p5"]

    item_ids = []
    word_indices = []
    rois = []

    for text_id in texts:
        text_limits = limits[text_id]
        max_roi = (text_limits[1][-1])  # end of the last word, i.e. maximal roi number
        iter_rois = range(1, max_roi + 1)  # all rois

        # iterate over all rois (i.e. all char ids) in one text
        for roi in iter_rois:
            # word index in text
            word_index = roi2word(roi, text_limits)

            word_indices.append(word_index)
            item_ids.append(text_id)
            rois.append(roi)

    data_dict = {
        'text_id': item_ids,
        'word_index_in_text': word_indices,
        'char_index_in_text': rois
    }

    data_df = pd.DataFrame(data_dict)
    data_df.to_csv(output_file, sep='\t', index=False)


def create_parser():
    base_path = Path(os.getcwd()).parent
    pars = argparse.ArgumentParser()

    pars.add_argument(
        '--limits-file',
        default=base_path / 'preprocessing_scripts/word_limits.json',
    )

    pars.add_argument(
        '--output-file',
        default=base_path / 'preprocessing_scripts/mappingRoiToWordIndex.csv',
    )

    return pars


if __name__ == '__main__':
    parser = create_parser()
    args = vars(parser.parse_args())

    char_index_to_word_index(**args)
