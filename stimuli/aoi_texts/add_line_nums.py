"""
This script add the line numbers to the individual aois in the .ias files. As the texts of the eye-tracking experiment
are presented on several lines, the line numbers are needed to plot and properly analyze the aois.
"""

from pathlib import Path

import pandas as pd


def add_line_numbers_to_aoi(aoi_folder_path='stimuli/aoi_texts/'):
    """
    Add line numbers to the aoi files in the given folder.
    :param aoi_folder_path: The path to the folder containing the aoi files.
    """
    # Get all .ias files in the folder
    aoi_files = Path(aoi_folder_path).glob('*.ias')

    for aoi_file in aoi_files:
        csv = pd.read_csv(aoi_file, sep='\t', encoding='utf8')
        # iterate over the rows. the line numbers starts with 1 and
        # increase by 1 as soon as the column start_y increases
        csv['line'] = 0
        start_y = 0
        line = 0
        for index, row in csv.iterrows():
            if row['start_y'] > start_y:
                line += 1
                start_y = row['start_y']
            csv.at[index, 'line'] = line

        # Save the modified DataFrame back to the .ias file
        csv.to_csv(aoi_file, sep='\t', index=False, encoding='utf8')


if __name__ == '__main__':
    path = Path(__file__).parent
    add_line_numbers_to_aoi(str(path))
