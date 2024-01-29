#!/usr/bin/env python3
"""
#TODO
Call: #TODO
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import pandas as pd


def create_word_aoi_limits(
        word_features_folder: str | Path,
        output_file_wl: str | Path,
        output_file_sl: str | Path,
) -> None:
    wf_paths = list(Path(word_features_folder).glob('*.tsv'))

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

            # 'word_limit_char_indices' stores the start and end aoi of a word
            word_start_aoi, word_end_aoi = word_row['word_limit_char_indices'].split(',')

            # if a punctuation mark directly precedes a word, a fixation on it is counted as a fixation on this word
            word_limits[0].append(int(word_start_aoi) - len(punctuation_before) // 2)

            # if a punctuation mark directly follows a word, a fixation on it is counted as a fixation on the word
            word_limits[1].append(int(word_end_aoi) + len(punctuation_after) // 2)

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


def main() -> int:
    base_path = Path(__file__).parent.parent

    word_features = base_path / 'stimuli' / 'word_features'
    output_wl = base_path / 'preprocessing_scripts/word_limits.json'
    output_sl = base_path / 'preprocessing_scripts/sent_limits.json'

    create_word_aoi_limits(
        word_features,
        output_wl,
        output_sl
    )

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
