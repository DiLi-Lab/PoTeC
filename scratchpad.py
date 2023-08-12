"""
to be deleted when everything is done, I'm just using it to the check the data types and the nan values in all csv files
+ print the markdown table + some other checks
"""

from pathlib import Path

import pandas as pd

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
    # 'stimuli/aoi_texts/aoi/',
    #'stimuli/word_features/',
    #'stimuli/text_tags/',
    # 'eyetracking_data/fixations/',
    # 'eyetracking_data/reader_rm_wf/',
    #'eyetracking_data/reading_measures/',
    #'eyetracking_data/scanpaths/',
    #'eyetracking_data/scanpaths_reader_rm_wf/',
]


def check_column_names_type():
    with open('cols_and_data_type.txt', 'w', encoding='utf8') as f:

        for path in PATHS:
            f.write(f'## {path}\n')

            try:
                csv = pd.read_csv(path, sep=r'\s+')
                f.write('## delimiter = spaces\n\n')
            except:
                csv = pd.read_csv(path, sep='\t')
                f.write('## delimiter = tab\n\n')

            cols = [c for c in csv.columns]
            new_df = pd.DataFrame(
                {'Column': cols, 'Data type': [dt for dt in csv.dtypes], 'Description': [pd.NA for _ in cols]})
            text = new_df.to_markdown(index=False)

            f.write(text)
            f.write('\n\n\n')


def check_word_text_cols():
    paths = Path('stimuli/word_features').glob('*.txt')

    with open('word-features_word!=text.txt', 'w', encoding='utf8') as f:
        for path in paths:
            csv = pd.read_csv(path, sep=r'\s+', na_filter=False)

            texts, words = csv['Text'], csv['Word']

            for idx, (text, word) in enumerate(zip(texts, words)):
                if text != word:
                    f.write(f'{path}\n')
                    f.write(f'Line: {idx + 2}\n')
                    f.write(f'Text: {text}\tWord: {word}\n\n')


def check_col_vals():
    for folder in PATHS_FOLDERS:
        cols = []

        for path in Path(folder).iterdir():

            try:
                csv = pd.read_csv(path, sep=r'\s+', keep_default_na=False, na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan'])
                # f.write('## delimiter = spaces\n\n')
            except:
                try:
                    csv = pd.read_csv(path, sep='\t', keep_default_na=False, na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan'])
                    # f.write('## delimiter = tab\n\n')
                except:
                    print(path)
                    print('\n')
                    continue

            # cur_cols = [c for c in csv.columns]
            # if cur_cols != cols:
            #     print(path)
            #     print(csv.columns)
            #     cols = cur_cols

            nans = csv.isna().sum().sum()
            if nans != 0:
                print(path)
                print(f'total nans: {nans}')
                counts = csv.isna().sum()
                print(counts[counts != 0])
                print(csv.shape)

                print('\n\n')


if __name__ == '__main__':
    # check_column_names_type()
    # check_word_text_cols()
    check_col_vals()
