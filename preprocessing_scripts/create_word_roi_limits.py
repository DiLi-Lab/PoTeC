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
        word_features_folder: str,
        output_file_wl: str,
        output_file_sl: str,
) -> None:
    wf_paths = list(Path(word_features_folder).glob('*.csv'))

    word_limits_dict = {}
    sent_limits_dict = {}

    for wf_file in wf_paths:

        text_id = wf_file.stem[-2:]

        # read file
        wf_csv = pd.read_csv(wf_file, sep='\t')

        word_limits = [[], []]
        sent_limits = [[1], []]

        for word_index, word_row in wf_csv.iterrows():

            punctuation_before = word_row['STTS_punctuation_before']
            punctuation_after = word_row['STTS_punctuation_after']

            if not punctuation_before or pd.isnull(punctuation_before):
                punctuation_before = ''  # replace "None" with nothing (because length is used below)
            if not punctuation_after or pd.isnull(punctuation_after):
                punctuation_after = ''

            # 'Position' stores the start and end roi of a word
            word_start_roi, word_end_roi = word_row['word_limit_char_indices'].split(',')

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
        '--word_features-folder', '-wf',
        default=base_path / 'stimuli/word_features',
    )

    pars.add_argument(
        '--output-file_wl', '-ow',
        default=base_path / 'preprocessing_scripts/word_limits.json',
    )

    pars.add_argument(
        '--output-file_sl', '-os',
        default=base_path / 'preprocessing_scripts/sent_limits.json',
    )

    return pars


if __name__ == '__main__':
    parser = create_parser()
    args = vars(parser.parse_args())

    create_word_roi_limits(**args)
