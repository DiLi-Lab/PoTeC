"""
to be deleted when everything is done, I'm just using it to the check the data types and the nan values in all csv files
+ print the markdown table + some other checks
"""
import json
from pathlib import Path

import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

PATHS = [
    'stimuli/aoi_texts/aoi/b0.ias',
    'stimuli/word_features/word_features_b0.txt',
    'stimuli/text_tags/b0.tags',
    'participants/participant_data.csv',
    'eyetracking_data/fixations/reader0_b0_fixations.txt',
    'eyetracking_data/reader_rm_wf/reader0_b0_merged.txt',
    'eyetracking_data/reading_measures/reader0_b0_rm.csv',
    'eyetracking_data/scanpaths/reader0_b0_scanpath.txt',
    'eyetracking_data/scanpaths_reader_rm_wf/reader0_b0_merged_sp_rm.txt',
]

PATHS_FOLDERS = [
    'stimuli/aoi_texts/aoi/',
    'stimuli/word_features/',
    'stimuli/text_tags/',
    'eyetracking_data/fixations/',
    'eyetracking_data/reader_rm_wf/',
    'eyetracking_data/reading_measures/',
    'eyetracking_data/scanpaths/',
    'eyetracking_data/scanpaths_reader_rm_wf/',
]


def check_column_names_type():
    unique_cols = set()
    with open('cols_and_data_type.txt', 'w', encoding='utf8') as f:

        for path in PATHS:
            f.write(f'## {path}\n')

            delimiters = ['\t', r'\s+', ',', ';']
            for idx, delimiter in enumerate(delimiters):
                csv = pd.read_csv(path, sep=delimiter)
                cols = csv.columns
                if len(cols) > 1:
                    break

            f.write(f'## delimiter = {delimiters[idx], idx}\n\n')

            cols = [c for c in csv.columns]
            unique_cols.update(cols)
            new_df = pd.DataFrame(
                {'Column': cols, 'Data type': [dt for dt in csv.dtypes], 'Description': [pd.NA for _ in cols]})
            text = new_df.to_markdown(index=False)

            f.write(text)
            f.write('\n\n\n')

    actual_cols = sorted(unique_cols)
    new_cols = [pd.NA for _ in actual_cols]

    new_df = pd.DataFrame({'Actual name': actual_cols, 'New name': new_cols})
    new_df.to_csv('new_col_mapping.csv', index=False)


def check_word_text_cols(path, col1, col2):
    # paths = Path('stimuli/word_features').glob('*.txt')
    paths = Path('eyetracking_data/reader_rm_wf/').glob('*.txt')

    w1 =
    w2 =

    with open('word-features_WordIndexInSentence!=WordIndexSent.txt', 'w', encoding='utf8') as f:
        for path in paths:
            csv = pd.read_csv(path, sep=r'\s+', na_filter=False)

            texts, words = csv['WordIndexInSentence'], csv['Word']

            for idx, (text, word) in enumerate(zip(texts, words)):
                if text != word:
                    f.write(f'{path}\n')
                    f.write(f'Line: {idx + 2}\n')
                    f.write(f'Text: {text}\tWord: {word}\n\n')


def check_col_vals():
    delimiters = ['\t', r'\s+', ',', ';']
    values = {}
    for folder in PATHS_FOLDERS:
        values[folder] = {}

        for path in tqdm(Path(folder).iterdir(), desc=f'Checking files in {folder}'):

            if path.suffix not in ['.txt', '.csv', '.ias', '.tags']:
                continue
            for idx, delimiter in enumerate(delimiters):
                csv = pd.read_csv(path, sep=delimiter, keep_default_na=False,
                                  na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND',
                                             '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan'])
                if len(csv.columns) > 1:
                    break

            for col in csv.columns:
                try:
                    values[folder][col] += csv[col].tolist()
                except KeyError:
                    values[folder][col] = csv[col].tolist()

            if csv[col].dtype in ['float64']:
                csv[col].plot.kde()
                plt.show()


if __name__ == '__main__':
    # paths = Path('stimuli/word_features').glob('*.txt')
    # word, text
    paths = Path('eyetracking_data/reader_rm_wf/').glob('*.txt')

    paths = [

    ]
    col1 = []
    col2 =[]

    check_column_names_type()
    #check_word_text_cols()
    #check_col_vals()
