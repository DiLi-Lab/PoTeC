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


# Aufruf: python create_word_roi_limits.py

def create_word_roi_limits(
        text_tags_folder: str,
        output_file_wl: str,
        output_file_sl: str,
) -> None:
    text_tags_paths = list(Path(text_tags_folder).glob('*.tags'))

    word_limits_dict = {}
    sent_limits_dict = {}

    for text_tags_file in text_tags_paths:

        text_id = text_tags_file.stem

        # read file
        text_tags_csv = pd.read_csv(text_tags_file, sep='\t')

        word_limits = [[], []]
        sent_limits = [[1], []]

        for word_index, word_row in text_tags_csv.iterrows():

            punctuation_before = word_row['STTS_Punctuationbefore']
            punctuation_after = word_row['STTS_Punctuationafter']

            if not punctuation_before or pd.isnull(punctuation_before):
                punctuation_before = ''  # replace "None" with nothing (because length is used below)
            if not punctuation_after or pd.isnull(punctuation_after):
                punctuation_after = ''

            # 'Position' stores the start and end roi of a word
            word_start_roi, word_end_roi = word_row['Position'].split(',')

            # if a punctuation mark directly precedes a word, a fixation on it is counted as a fixation on this word
            word_limits[0].append(int(word_start_roi) - len(punctuation_before) // 2)

            # if a punctuation mark directly follows a word, a fixation on it is counted as a fixation on the word
            word_limits[1].append(int(word_end_roi) + len(punctuation_after) // 2)

            # If word is followed by a sentence closing punctuation mark (tagged as $.), start new sentence
            if '$.' in punctuation_after:
                sent_limits[1].append(word_index + 1)
                sent_limits[0].append(word_index + 2)

        sent_limits[0] = sent_limits[0][:-1]  # den letzte angefangenen gabs gar nicht.

        word_limits_dict[text_id] = word_limits
        sent_limits_dict[text_id] = sent_limits

    with open(output_file_wl, 'w') as word_limits_file:
        json.dump(word_limits_dict, word_limits_file, indent=2, sort_keys=True)

    with open(output_file_sl, 'w') as sent_limits_file:
        json.dump(sent_limits_dict, sent_limits_file, indent=2, sort_keys=True)


def create_parser():
    base_path = Path(os.getcwd()).parent
    pars = argparse.ArgumentParser()

    pars.add_argument(
        '--text-tags-folder',
        default=base_path / 'stimuli/text_tags',
    )

    pars.add_argument(
        '--output-file_wl',
        default=base_path / 'preprocessing_scripts/word_limits.json',
    )

    pars.add_argument(
        '--output-file_sl',
        default=base_path / 'preprocessing_scripts/sent_limits.json',
    )

    return pars


if __name__ == '__main__':
    parser = create_parser()
    args = vars(parser.parse_args())

    create_word_roi_limits(**args)
