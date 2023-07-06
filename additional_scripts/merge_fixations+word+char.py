#!/usr/bin/env python3
"""
RUNNING INSTRUCTIONS
This script is used to merge the fixation data with the word and character information.
If the repo is downloaded as-is, the script can be run in this folder and no paths need to be provided.

python3 merge_fixations+word+char.py

You can also specify the paths to some or all the files you need yourself. In that case ouy need to make sure that the
files contain all the information they are expected to contain as specified in the docstring.

python3 merge_fixations+word+char.py
    --fixation_folder /path/to/fixation/folder
    --roi2word_file /path/to/roi2word/file
    --texts_folder /path/to/texts/folder
    --ias_folder /path/to/ias/folder
    --output_folder /path/to/output/folder

If a roi (which is equivalent to CharIndexInText) cannot be mapped to a character, the values will be written as np.NA in the output file.
All errors will be logged in a file in the errors folder.
"""

import argparse
import os
import re
from pathlib import Path

import pandas as pd
from tqdm import tqdm


def create_scanpaths(
        fixation_folder: str,
        roi2word_file: str,
        texts_folder: str,
        ias_folder: str,
        output_folder: str,
) -> None:
    """
    This function adds the word and character information to the fixation data.
    The output is a file containing the scanpath for each reader and each text.

    Parameters
    ----------
    fixation_folder: str
        Files are expected to contain the following columns:
        'roi',
    roi2word_file: str
        Expected to contain the following columns:
        'itemid', 'wordIndexInText', 'charIndexInText'
    texts_folder: str
        Files are expected to contain the following columns:
        'WORD_INDEX', 'WORD'
    ias_folder: str
        Interest area files are expected to contain the following columns:
        'type', 'roi', 'start_x', 'start_y', 'end_x', 'end_y', 'character'
    output_folder: str
        Path to the folder where the output files should be saved.

    """

    # create the output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if not os.path.exists('errors'):
        os.makedirs('errors')

    with open('errors/merge_fixations_word_char_errors.txt', 'w') as f:
        f.write(
            'For the fixation files in this file, there were errors '
            'when trying to map the roi to a word and character.'
            'Those need to be manually fixed. The missing values are written as np.NA in the output file.\n\n'
            )

        f.write('fixation_file_name, text_id, roi, word_idx, word, character')

    # sort the file names to be sure we have the same order
    fixation_files = sorted(list(Path(fixation_folder).glob('*.txt')))

    roi2word = pd.read_csv(roi2word_file, sep='\t')

    for fixation_file in tqdm(fixation_files):
        # get only the file name without the path
        fixation_file_name = os.path.basename(fixation_file)
        fix_csv = pd.read_csv(fixation_file, sep='\s+')

        # extract text id from file name which is r'(bp)\d'
        text_id = fixation_file_name.split('_')[1]

        text_file = Path(texts_folder) / f'{text_id}.tags'
        text_csv = pd.read_csv(text_file, sep='\t')

        # get aoi file for the text
        aoi_file = Path(ias_folder) / f'{text_id}.ias'
        aoi_csv = pd.read_csv(
            aoi_file,
            sep='\t',
            names=['type', 'roi', 'start_x', 'start_y', 'end_x', 'end_y', 'character'],
        )

        new_columns = {
            'wordIndexInText': [],
            'sentIndex': [],
            'charIndexInText': [],
            'word': [],
            'character': [],
        }

        for idx in range(len(fix_csv)):
            roi = fix_csv.iloc[idx]['roi']

            try:
                # map roi (=char index) to word index
                word_idx = roi2word[(roi2word['charIndexInText'] == roi)
                                    & (roi2word['itemid'] == text_id)]['wordIndexInText'].values[0]

                # get the actual character and word
                character = aoi_csv[aoi_csv['roi'] == roi]['character'].values[0]
                word = text_csv[text_csv['WORD_INDEX'] == word_idx]['WORD'].values[0]
                sentence_index = text_csv[text_csv['WORD_INDEX'] == word_idx]['SentenceIndex'].values[0]

            # in case the roi does not exist, there will be an index error
            except IndexError:
                word_idx, word, character, sentence_index = pd.NA, pd.NA, pd.NA, pd.NA
                with open('errors/merge_fixations_word_char_errors.txt', 'a') as f:
                    f.write(f'\n{fixation_file_name}, {text_id}, {roi}, {word_idx}, {word}, {character}')

            new_columns['wordIndexInText'].append(word_idx)
            new_columns['charIndexInText'].append(roi)
            new_columns['word'].append(word)
            new_columns['character'].append(character)
            new_columns['sentIndex'].append(sentence_index)

        new_df = pd.DataFrame(new_columns)
        fix_csv = pd.concat([fix_csv, new_df], axis=1)

        scanpath_file = re.sub('fixations', 'scanpath', fixation_file_name)

        fix_csv.to_csv(Path(output_folder) / scanpath_file, sep='\t', index=False)


def create_parser():
    base_path = Path(os.getcwd()).parent
    pars = argparse.ArgumentParser()

    pars.add_argument(
        '--fixation-folder',
        default=base_path / 'eyetracking_data/fixations/',
        help='Path to fixation data'
    )

    pars.add_argument(
        '--roi2word-file',
        default=base_path / 'preprocessing_scripts/mappingRoiToWordIndex.csv',
    )

    pars.add_argument(
        '--texts-folder',
        default=base_path / 'stimuli/text_tags/',
    )

    pars.add_argument(
        '--ias-folder',
        default=base_path / 'stimuli/aoi_texts/aoi/'
    )

    pars.add_argument(
        '--output-folder',
        default=base_path / 'eyetracking_data/scanpaths/',
    )

    return pars


if __name__ == '__main__':
    parser = create_parser()
    args = vars(parser.parse_args())

    create_scanpaths(**args)
