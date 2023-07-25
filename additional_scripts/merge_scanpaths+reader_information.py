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
        reader_information_file: str,
        output_folder: str,
) -> None:
    # create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    participant_data = pd.read_csv(reader_information_file, sep=';')

    scanpath_files = Path(scanpaths_folder).glob('*.txt')

    for scanpath_file in tqdm(scanpath_files, total=900):
        scanpath_file_name = os.path.basename(scanpath_file)
        reader_id = re.search(r'(\d+)_', scanpath_file_name).group(1)

        reader_data = participant_data[participant_data['participant_id'] == int(reader_id)]

        scanpath = pd.read_csv(scanpath_file, sep='\t')
        # create a df out of the reading data that has the same length as the scanpath file

        # TODO: finish script


def create_parser():
    base_path = Path(os.getcwd()).parent
    pars = argparse.ArgumentParser()

    pars.add_argument(
        '--scanpaths-folder',
        default=base_path / 'eyetracking_data/scanpaths/',
    )

    pars.add_argument(
        '--reader-information-file',
        default=base_path / 'participants_info/participant_data.csv',
    )

    pars.add_argument(
        '--output-folder',
        default=base_path / 'eyetracking_data/scanpaths_reader_info/',
    )

    return pars


if __name__ == '__main__':
    parser = create_parser()
    args = vars(parser.parse_args())

    merge_scanpaths_reader_information(**args)
