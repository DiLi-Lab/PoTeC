#!/usr/bin/env python3
"""

Before running this script you need to run the following script:
python generate_scanpaths.py
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
        output_folder: str,
) -> None:
    # create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    scanpath_files = Path(scanpaths_folder).glob('*.tsv')

    for scanpath_file in tqdm(scanpath_files, total=900):
        scanpath_file_name = os.path.basename(scanpath_file)

        name_components = scanpath_file_name.split('_')
        rm_filename = f'{name_components[0]}_{name_components[1]}_merged.tsv'

        final_file_name = f'{name_components[0]}_{name_components[1]}_merged_sp_rm.tsv'

        scanpath_csv = pd.read_csv(scanpath_file, sep='\t')
        rm_csv = pd.read_csv(Path(rm_folder) / rm_filename, sep='\t')

        scanpath_csv['trial'] = scanpath_csv['trial'].astype(int)
        rm_csv['trial'] = rm_csv['trial'].astype(int)

        merged_df = pd.merge(scanpath_csv, rm_csv,
                             how='inner',
                             left_on=['word_index_in_text', 'sent_index_in_text'],
                             right_on=['word_index_in_text', 'sent_index_in_text'],
                             suffixes=(None, '_rm'),
                             )
        merged_df = merged_df.sort_values(by=['fixation_index'])

        merged_df = merged_df.drop(
            columns=[col for col in merged_df.columns if col.endswith('_rm')],
        )

        merged_df.to_csv(Path(output_folder) / final_file_name, sep='\t', index=False, na_rep='NA')


def create_parser():
    base_path = Path(os.getcwd()).parent
    pars = argparse.ArgumentParser()

    pars.add_argument(
        '--scanpaths-folder', '-sp',
        default=base_path / 'eyetracking_data/scanpaths/',
    )

    pars.add_argument(
        '--rm-folder', '-rm',
        default=base_path / 'eyetracking_data/reader_rm_wf/',
    )

    pars.add_argument(
        '--output-folder', '-o',
        default=base_path / 'eyetracking_data/scanpaths_reader_rm_wf/',
    )

    return pars


if __name__ == '__main__':
    parser = create_parser()
    args = vars(parser.parse_args())

    merge_scanpaths_reader_information(**args)
