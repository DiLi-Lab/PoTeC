#!/usr/bin/env python3
"""

Before running this script you need to run the following script:
python merge_fixations+word+char.py
Call: TODO
"""

import argparse
import os
import re
from pathlib import Path

import pandas as pd
from tqdm import tqdm


def merge_scanpaths_reader_information(
        scanpaths_folder: str,
        rm_folder: str,
        reader_information_file: str,
        output_folder: str,
) -> None:
    # create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    participant_data = pd.read_csv(reader_information_file, sep=',')

    scanpath_files = Path(scanpaths_folder).glob('*.txt')

    for scanpath_file in tqdm(scanpath_files, total=900):
        scanpath_file_name = os.path.basename(scanpath_file)
        reader_id = re.search(r'(\d+)_', scanpath_file_name).group(1)

        name_components = scanpath_file_name.split('_')
        rm_filename = f'{name_components[0]}_{name_components[1]}_merged.txt'

        final_file_name = f'{name_components[0]}_{name_components[1]}_merged_sp_rm.txt'

        reader_data = participant_data[participant_data['readerId'] == int(reader_id)]

        scanpath_csv = pd.read_csv(scanpath_file, sep='\t')
        rm_csv = pd.read_csv(Path(rm_folder) / rm_filename, sep='\t')

        scanpath_csv['trial'] = scanpath_csv['trial'].astype(int)
        rm_csv['trial'] = rm_csv['trial'].astype(int)

        merged_df = pd.merge(scanpath_csv, rm_csv,
                             how='inner',
                             left_on=['wordIndexInText', 'sentIndex'],
                             right_on=['WordIndexInText', 'SentenceIndex'],
                             suffixes=(None, '_rm'),
                             )
        merged_df = merged_df.sort_values(by=['CURRENT_FIX_INDEX'])

        merged_df = merged_df.drop(
            columns=[col for col in merged_df.columns if col.endswith('_rm')],
        )

        merged_df.to_csv(Path(output_folder) / final_file_name, sep='\t', index=False)


def create_parser():
    base_path = Path(os.getcwd()).parent
    pars = argparse.ArgumentParser()

    pars.add_argument(
        '--scanpaths-folder',
        default=base_path / 'eyetracking_data/scanpaths/',
    )

    pars.add_argument(
        '--rm-folder',
        default=base_path / 'eyetracking_data/rm_word_features/',
    )

    pars.add_argument(
        '--reader-information-file',
        default=base_path / 'participants/participant_data.csv',
    )

    pars.add_argument(
        '--output-folder',
        default=base_path / 'eyetracking_data/scanpaths_reader_rm/',
    )

    return pars


if __name__ == '__main__':
    parser = create_parser()
    args = vars(parser.parse_args())

    merge_scanpaths_reader_information(**args)
