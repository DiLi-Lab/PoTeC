#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

import pandas as pd
from tqdm import tqdm


def split_fixation_report(
        fixation_report_file: str | Path,
        output_folder: str | Path,
        columns: list,
) -> None:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    new_col_names = {
        'itemid': 'item_id',
        'ACC_B_Q1': 'acc_bq_1',
        'ACC_B_Q2': 'acc_bq_2',
        'ACC_B_Q3': 'acc_bq_3',
        'ACC_T_Q1': 'acc_tq_1',
        'ACC_T_Q2': 'acc_tq_2',
        'ACC_T_Q3': 'acc_tq_3',
        'CURRENT_FIX_DURATION': 'fixation_duration',
        'NEXT_SAC_DURATION': 'next_saccade_duration',
        'PREVIOUS_SAC_DURATION': 'previous_saccade_duration',
        'RECORDING_SESSION_LABEL': 'reader_id',
        'CURRENT_FIX_INTEREST_AREA_INDEX': 'aoi',
        'topic': 'text_domain',
        'CURRENT_FIX_INDEX': 'fixation_index',
        'CURRENT_FIX_X': 'fixation_position_x',
        'CURRENT_FIX_Y': 'fixation_position_y',
    }

    fix_rep_csv = pd.read_csv(fixation_report_file, sep='\t', index_col=False)
    reader_ids = set()  # save readerIds to write into a separate file (for later use)

    reader_ids_item_ids = set()  # set to store all already seen reader and itemids (used below to first write col names
    # when a text read by a reader is encountered for the first time

    output_file_name = ''

    header = fix_rep_csv.columns.values.tolist()
    reader_item_df = pd.DataFrame(columns=header)

    for index, row in tqdm(fix_rep_csv.iterrows(), desc='Splitting report: '):

        reader_id = str(row['RECORDING_SESSION_LABEL'])
        item_id = row['itemid']
        reader_item = str(reader_id) + item_id  # combination of reader and itemid

        if reader_item not in reader_ids_item_ids:
            # dump last reader-item df to file unless it is the first reader and item
            if not reader_item_df.empty:
                reader_item_df = reader_item_df[columns]
                reader_item_df.reindex(columns=columns)
                reader_item_df.rename(columns=new_col_names, inplace=True)
                reader_item_df.to_csv(output_file_name, sep='\t', index=False)

            reader_item_df = pd.DataFrame(columns=header)
            output_file_name = Path(output_folder) / (
                    'reader' + reader_id + '_' + item_id + '_uncorrected_fixations.tsv')
            reader_ids.add(reader_id)  # save readerId if encountered for the first time
            reader_ids_item_ids.add(reader_item)  # save reader-item combination if encountered for the first time

        reader_item_df = pd.concat([reader_item_df, row.to_frame().T], ignore_index=False)

    reader_item_df = reader_item_df[columns]
    reader_item_df.reindex(columns=columns)
    reader_item_df.rename(columns=new_col_names, inplace=True)
    reader_item_df.to_csv(output_file_name, sep='\t', index=False)


def main():
    repo_root = Path(__file__).parent.parent

    columns = ['CURRENT_FIX_INDEX', 'topic', 'trial', 'ACC_B_Q1', 'ACC_B_Q2', 'ACC_B_Q3', 'ACC_T_Q1', 'ACC_T_Q2',
               'ACC_T_Q3', 'CURRENT_FIX_DURATION', 'NEXT_SAC_DURATION', 'PREVIOUS_SAC_DURATION', 'version',
               'CURRENT_FIX_INTEREST_AREA_INDEX', 'RECORDING_SESSION_LABEL', 'itemid', 'CURRENT_FIX_X',	'CURRENT_FIX_Y']
    output_folder = repo_root / 'eyetracking_data/fixations_uncorrected/'
    fixation_report_file = repo_root / 'eyetracking_data/original_uncorrected_fixation_report.txt'

    split_fixation_report(fixation_report_file, output_folder, columns)


if __name__ == '__main__':
    main()
