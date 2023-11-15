#!/usr/bin/env python3
"""
TODO: clean again, r is never closed?
Call: python3 merge_rm_wf.py
To specify custom file paths see argparse arguments at the bottom of the file.
"""
from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

import pandas as pd
from tqdm import tqdm


def merge_rm_word_features(
        reading_measure_folder: str | Path,
        word_features_folder: str | Path,
        participants_file: str | Path,
        output_folder: str | Path,
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    reader_ids = pd.read_csv(participants_file, sep='\t', usecols=['reader_id'])['reader_id'].tolist()

    texts = ['b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'p0', 'p1', 'p2', 'p3', 'p4', 'p5']

    # Read and merge data

    # Read text features
    for textIndex, text in tqdm(enumerate(texts), desc='Merging files...', total=len(texts)):
        filename_features = os.path.join(word_features_folder, 'word_features_' + text + '.tsv')

        word_features = pd.read_csv(
            filename_features, sep='\t', keep_default_na=False,
            na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND',
                       '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan', ''],
            encoding='utf-8',
            engine='python',
        )

        word_features = word_features.drop(columns=['text_id', 'word_limit_char_indices'])

        # replace missing values with 0s (affects frequency measures: if word does not occur in corpus, frequency = 0)
        word_features = word_features.fillna(0)

        # add Eye movements data for each reader
        for readerIndex, reader in enumerate(reader_ids):
            filename_reading_measures = os.path.join(
                reading_measure_folder,
                'reader' + str(reader) + '_' + text + '_rm.tsv'
            )

            reading_measure_csv = pd.read_csv(
                filename_reading_measures,
                sep='\t',
                keep_default_na=False,
                na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND',
                           '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan', ''],
            )

            # sort columns. Necessary because different col ordering in different input files
            reading_measure_csv = reading_measure_csv[
                ["word_index_in_sent", "sent_index_in_text", "FFD", "SFD", "FD", "FPRT", "FRT", "TFT", "RRT", "RPD_inc",
                 "RPD_exc",
                 "RBRT", "Fix", "FPF", "RR", "FPReg", "TRC_out", "TRC_in", "LP", "SL_in", "SL_out", "acc_bq_1",
                 "acc_bq_2", "acc_bq_3", "acc_tq_1", "acc_tq_2", "acc_tq_3", "mean_acc_tq", "mean_acc_bq",
                 "text_domain_numeric",
                 "trial",
                 "text_id", "reader_id", "gender_numeric", "reader_domain_numeric", "age", "expert_status_numeric",
                 "domain_expert_status_numeric"]
            ]

            # concatenate text features with eye movements
            merged_df = pd.merge(word_features, reading_measure_csv,
                                 how='inner',
                                 left_on=['word_index_in_sent', 'sent_index_in_text'],
                                 right_on=['word_index_in_sent', 'sent_index_in_text'],
                                 suffixes=(None, '_rm'),
                                 )

            # write merged data
            filename_merged_data = os.path.join(output_folder, 'reader' + str(reader) + '_' + text + '_merged.tsv')
            merged_df.to_csv(path_or_buf=filename_merged_data, header=True, na_rep='NA', sep='\t', index=False)


def main() -> int:
    repo_root = Path(__file__).parent.parent

    reading_measure_folder = repo_root / 'eyetracking_data/reading_measures'
    word_features_folder = repo_root / 'stimuli/word_features'
    participants_file = repo_root / 'participants/participant_data.tsv'
    output_folder = repo_root / 'eyetracking_data/reading_measures_merged'

    merge_rm_word_features(
        reading_measure_folder=reading_measure_folder,
        word_features_folder=word_features_folder,
        participants_file=participants_file,
        output_folder=output_folder,
    )

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
