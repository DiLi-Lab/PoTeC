#!/usr/bin/env python3
"""
Creates scanpaths for given fixations files and text information.
Call: python3 generate_scanpaths.py
To specify custom file paths see argparse below.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import pandas as pd
from tqdm import tqdm


def create_scanpaths(
        fixation_folder: str | Path,
        aoi2word_file: str | Path,
        wf_folder: str | Path,
        ias_folder: str | Path,
        output_folder: str | Path,
) -> None:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # sort the file names to be sure we have the same order
    fixation_files = sorted(list(Path(fixation_folder).glob('*.tsv')))

    aoi2word = pd.read_csv(aoi2word_file, sep='\t')

    for fixation_file in tqdm(fixation_files):
        # get only the file name without the path
        fixation_file_name = os.path.basename(fixation_file)
        fix_csv = pd.read_csv(fixation_file, sep='\t')

        # extract text id from file name which is r'(bp)\d'
        text_id = fixation_file_name.split('_')[1]

        wf_file = Path(wf_folder) / f'word_features_{text_id}.tsv'
        wf_csv = pd.read_csv(wf_file, sep='\t', keep_default_na=False,
                             na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND',
                                        '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan', ''])

        # get aoi file for the text
        aoi_file = Path(ias_folder) / f'{text_id}.ias'
        aoi_csv = pd.read_csv(
            aoi_file,
            sep='\t',
        )

        new_columns = {
            'word_index_in_text': [],
            'sent_index_in_text': [],
            'char_index_in_text': [],
            'word': [],
            'character': [],
        }
        for idx in range(len(fix_csv)):
            aoi = fix_csv.iloc[idx]['aoi']

            # map aoi (=char index) to word index
            word_idx = aoi2word[(aoi2word['char_index_in_text'] == aoi)
                                & (aoi2word['text_id'] == text_id)]['word_index_in_text'].values[0]

            # get the actual character and word
            character = aoi_csv[aoi_csv['aoi'] == aoi]['character'].values[0]
            word = wf_csv[wf_csv['word_index_in_text'] == word_idx]['word'].values[0]
            sentence_index = wf_csv[wf_csv['word_index_in_text'] == word_idx]['sent_index_in_text'].values[0]

            new_columns['word_index_in_text'].append(word_idx)
            new_columns['char_index_in_text'].append(aoi)
            new_columns['word'].append(word)
            new_columns['character'].append(character)
            new_columns['sent_index_in_text'].append(sentence_index)

        new_df = pd.DataFrame(new_columns)
        new_df['text_id_numeric'] = wf_csv['text_id_numeric'].iloc[0]
        new_df['text_domain_numeric'] = wf_csv['text_domain_numeric'].iloc[0]

        fix_csv = pd.concat([fix_csv, new_df], axis=1)

        if fix_csv['text_domain'].values[0] == 'bio':
            fix_csv['text_domain'] = 'biology'

        scanpath_file = re.sub('fixations', 'scanpath', fixation_file_name)

        fix_csv.to_csv(Path(output_folder) / scanpath_file, sep='\t', index=False, na_rep='NA')


def main() -> int:
    repo_root = Path(__file__).parent.parent

    # rewrite args as hardcoded paths using the repo root
    fixation_folder = repo_root / 'eyetracking_data/fixations/'
    aoi2word_file = repo_root / 'preprocessing_scripts/aoi_to_word.tsv'
    wf_folder = repo_root / 'stimuli/word_features/'
    ias_folder = repo_root / 'stimuli/aoi_texts/'
    output_folder = repo_root / 'eyetracking_data/scanpaths/'

    create_scanpaths(
        fixation_folder=fixation_folder,
        aoi2word_file=aoi2word_file,
        wf_folder=wf_folder,
        ias_folder=ias_folder,
        output_folder=output_folder,
    )

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
