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
        participants_file: str | Path,
        wf_folder: str | Path,
        ias_folder: str | Path,
        output_folder: str | Path,
) -> None:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # sort the file names to be sure we have the same order
    fixation_files = sorted(list(Path(fixation_folder).glob('*.tsv')))

    df_participants = pd.read_csv(participants_file, delimiter="\t")

    aoi2word = pd.read_csv(aoi2word_file, sep='\t')

    for fixation_file in tqdm(fixation_files, desc='Creating scanpaths'):
        # get only the file name without the path
        fixation_file_name = os.path.basename(fixation_file)
        fix_csv = pd.read_csv(fixation_file, sep='\t')

        # extract text id from file name which is r'(bp)\d'
        text_id = fix_csv['text_id'].iloc[0]
        reader_id = fix_csv['reader_id'].iloc[0]

        wf_file = Path(wf_folder) / f'word_features_{text_id}.tsv'
        # specifying the nan values like this is necessary, see README.md
        wf_csv = pd.read_csv(wf_file, sep='\t', keep_default_na=False,
                             na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND',
                                        '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan', ''])

        # get aoi file for the text
        aoi_file = Path(ias_folder) / f'{text_id}.ias'
        aoi_csv = pd.read_csv(
            aoi_file,
            sep='\t',
        )

        # new columns to be extracted from the aoi file
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
        # add some more columns that are the same for each row
        # text information
        text_id_num = wf_csv['text_id_numeric'].iloc[0]
        text_domain_num = wf_csv['text_domain_numeric'].iloc[0]
        new_df['text_id_numeric'] = text_id_num
        new_df['text_domain_numeric'] = text_domain_num

        # get reader information
        reader_row = df_participants.loc[df_participants['reader_id'] == reader_id]
        reader_discipline_numeric = reader_row['reader_discipline_numeric'].item()
        level_of_studies_numeric = reader_row['level_of_studies_numeric'].item()

        # if the text has been read by a domain expert, the label is 1=expert_reading, else 0=non-expert_reading
        expert_reading_label_numeric = 1 if level_of_studies_numeric == 1 and text_domain_num == reader_discipline_numeric \
            else 0
        expert_reading_label = 'expert_reading' if expert_reading_label_numeric == 1 else 'non-expert_reading'

        new_df['reader_discipline_numeric'] = reader_discipline_numeric
        new_df['level_of_studies_numeric'] = level_of_studies_numeric
        new_df['expert_reading_label_numeric'] = expert_reading_label_numeric
        new_df['expert_reading_label'] = expert_reading_label

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
    participants_file = repo_root / 'participants/participant_data.tsv'
    wf_folder = repo_root / 'stimuli/word_features/'
    ias_folder = repo_root / 'stimuli/aoi_texts/'
    output_folder = repo_root / 'eyetracking_data/scanpaths/'

    create_scanpaths(
        fixation_folder=fixation_folder,
        aoi2word_file=aoi2word_file,
        participants_file=participants_file,
        wf_folder=wf_folder,
        ias_folder=ias_folder,
        output_folder=output_folder,
    )

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
