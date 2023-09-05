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
    # 'stimuli/aoi_texts/aoi/b0.ias',
    'stimuli/word_features/word_features_b0.csv',
    'stimuli/text_tags/b0.csv',
    'participants/participant_data.csv',
    'eyetracking_data/fixations/reader0_b0_fixations.csv',
    'eyetracking_data/reader_rm_wf/reader0_b0_merged.csv',
    'eyetracking_data/reading_measures/reader0_b0_rm.csv',
    'eyetracking_data/scanpaths/reader0_b0_scanpath.csv',
    'eyetracking_data/scanpaths_reader_rm_wf/reader0_b0_merged_sp_rm.csv',
]

PATHS_FOLDERS = [
    # 'stimuli/aoi_texts/aoi/',
    'stimuli/word_features/',
    'stimuli/text_tags/',
    'eyetracking_data/fixations/',
    'eyetracking_data/reader_rm_wf/',
    'eyetracking_data/reading_measures/',
    'eyetracking_data/scanpaths/',
    'eyetracking_data/scanpaths_reader_rm_wf/',
]

DELIMITERS = ['\t', r'\s+', ',', ';']


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
                {'Column name': cols, 'Possible values': [dt for dt in csv.dtypes],
                 'Missing value': [pd.NA for _ in cols], 'Description': [pd.NA for _ in cols],
                 'Source': [pd.NA for _ in cols]})
            text = new_df.to_markdown(index=False)

            # new_df.to_csv('codebook_tables/' + path.split('/')[-1].split('.')[0] + '.csv', index=False)

            f.write(text)
            f.write('\n\n\n')

    actual_cols = sorted(unique_cols)
    new_cols = [pd.NA for _ in actual_cols]

    new_df = pd.DataFrame({'Actual name': actual_cols, 'New name': new_cols})
    new_df.to_csv('new_col_mapping-version2.csv', index=False)


def check_duplicate_cols(all_paths, cols1, cols2):
    for path, col1, col2 in zip(all_paths, cols1, cols2):

        files = Path(path).glob('*.csv')

        with open(f'stuff_to_check/mismatch_{Path(path).stem}_{col1}_{col2}.txt', 'w', encoding='utf8') as f:

            for path in files:

                csv = pd.read_csv(path, sep='\t', na_filter=False)

                c1, c2, word = csv[col1], csv[col2], csv['word']

                for idx, (v1, v2, w) in enumerate(zip(c1, c2, word)):
                    if v1.lower() != v2.lower():
                        f.write(f'{path}\n')
                        f.write(f'Line: {idx + 1}\n')
                        f.write(f'{col1}: {v1}\t{col2}: {v2}\tword:{w}\n\n')


def check_col_vals():
    values = {}
    for folder in PATHS_FOLDERS:
        values[folder] = {}

        for path in tqdm(Path(folder).glob('*.csv'), desc=f'Checking files in {folder}'):

            csv = pd.read_csv(path, sep='\t', keep_default_na=False,
                              na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND',
                                         '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan'])

            for col in csv.columns:
                try:
                    values[folder][col] += csv[col].tolist()
                except KeyError:
                    values[folder][col] = csv[col].tolist()

            # TODO rewrite to include all values from all files and plot those, NOT per file
            if csv[col].dtype in ['float64']:
                csv[col].plot.kde()
                plt.show()


def rename_cols_all_files():
    # load the mapping as csv and convert to dict with old value as key and new value as value
    mapping = pd.read_csv('new_col_mapping.csv')
    mapping = mapping.fillna('')
    mapping = dict(zip(mapping['Actual name'], mapping['New name']))

    for folder in PATHS_FOLDERS:
        for path in tqdm(Path(folder).glob('*.csv'), desc=f'Renaming files in {folder}'):

            csv = pd.read_csv(path, sep='\t', keep_default_na=False,
                              na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND',
                                         '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan'])

            rename = False
            for col in csv.columns:
                try:
                    new_name = mapping[col]
                    new_name = col.lower() if not new_name else new_name

                    csv.rename(columns={col: new_name}, inplace=True)
                    rename = True

                except KeyError:
                    continue

            if rename:
                path.rename(path.with_suffix('.csv'))
                csv.to_csv(path, sep='\t', index=False)


def clean_text_tags():
    paths = Path('stimuli/OLD/text_tags/').glob('*.csv')

    for path in paths:
        csv = pd.read_csv(path, sep='\t', keep_default_na=False,
                          na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND',
                                     '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan'])

        cols = csv.columns
        print(cols)

        if 'is_abbreviation.1' in cols and 'is_abbreviation' not in cols:
            csv.rename(columns={'is_abbreviation.1': 'is_abbreviation'}, inplace=True)
        elif 'is_abbreviation.1' in cols and 'is_abbreviation' in cols:
            csv.drop(columns=['is_abbreviation.1'], inplace=True)

        if 'word_index_in_text.1' in cols and 'word_index_in_text' not in cols:
            csv.rename(columns={'word_index_in_text.1': 'word_index_in_text'}, inplace=True)
        elif 'word_index_in_text.1' in cols and 'word_index_in_text' in cols:
            csv.drop(columns=['word_index_in_text.1'], inplace=True)

        csv.to_csv(path, sep='\t', index=False)
        print(csv.columns)


def merge_text_tags_wf():
    # iterate over all texts, then merge word_Features/word_features_b0.csv with text_tags/b0.csv for all texts
    for tag_path in tqdm(Path('stimuli/OLD/text_tags/').glob('*.csv'), desc='Merging text tags and word features'):
        filename = tag_path.stem
        word_features = pd.read_csv(f'stimuli/OLD/word_features/word_features_{filename}.csv', sep='\t')

        text_tags = pd.read_csv(tag_path, sep='\t')
        merged = pd.merge(word_features, text_tags, left_index=True, right_index=True)
        # rename text to word and drop word_y and word_x
        merged.rename({'text': 'word'}, axis=1, inplace=True)
        merged.drop(columns=['word_y', 'word_x', 'line_index', 'PRELS', 'PRELAT', 'PPOSAT', 'PPER', 'PPOSS', 'PIDAT',
                             'PIAT', 'PIS', 'PDAT', 'PDS', 'NN', 'NE', 'KOKOM',
                             'KON', 'KOUS', 'KOUI', 'ITJ', 'FM', 'CARD', 'ART', 'APZR', 'APPO', 'APPRART', 'APPR',
                             'ADV', 'ADJD', 'ADJA',
                             'XY', 'VMPP', 'VMINF', 'VMFIN', 'VAPP', 'VAFIN', 'VVPP', 'VVIZU', 'VVINF', 'VVIMP',
                             'VVFIN', 'TRUNC', 'PTKA',
                             'PTKANT', 'PTKVZ', 'PTKNEG', 'PTKZU', 'PAV', 'PWAV', 'PWAT', 'PWS', 'PRF', 'STTS-tag'], inplace=True)

        assert (len(merged) == len(word_features) == len(text_tags))

        merged = merged[['word', 'word_index_in_text', 'word_index_in_sent', 'sent_index_in_text',
                         'word_limit_char_indices', 'text_id', 'is_technical_term',
                         'word_length',
                         'STTS_punctuation_before',
                         'STTS_punctuation_after',  'is_in_quote',
                         'is_in_parentheses', 'is_clause_beginning', 'is_sent_beginning', 'is_abbreviation',
                         'contains_symbol', 'contains_hyphen',
                         'contains_abbreviation', 'STTS_PoS_tag',
                         'type', 'type_length_chars', 'PoS_tag', 'lemma', 'lemma_length_chars', 'syllables',
                         'type_length_syllables', 'annotated_type_frequency_normalized', 'type_frequency_normalized',
                         'lemma_frequency_normalized', 'familiarity_normalized', 'regularity_normalized',
                         'document_frequency_normalized', 'sentence_frequency_normalized',
                         'cumulative_syllable_corpus_frequency_normalized',
                         'cumulative_syllable_lexicon_frequency_normalized',
                         'cumulative_character_corpus_frequency_normalized',
                         'cumulative_character_lexicon_frequency_normalized',
                         'cumulative_character_bigram_corpus_frequency_normalized',
                         'cumulative_character_bigram_lexicon_frequency_normalized',
                         'cumulative_character_trigram_corpus_frequency_normalized',
                         'cumulative_character_trigram_lexicon_frequency_normalized',
                         'initial_letter_frequency_normalized',
                         'initial_bigram_frequency_normalized', 'initial_trigram_frequency_normalized',
                         'avg_cond_prob_in_bigrams',
                         'avg_cond_prob_in_trigrams', 'neighbors_coltheart_higher_freq_cum_freq_normalized',
                         'neighbors_coltheart_higher_freq_count_normalized',
                         'neighbors_coltheart_all_cum_freq_normalized',
                         'neighbors_coltheart_all_count_normalized',
                         'neighbors_levenshtein_higher_freq_cum_freq_normalized',
                         'neighbors_levenshtein_higher_freq_count_normalized',
                         'neighbors_levenshtein_all_cum_freq_normalized',
                         'neighbors_levenshtein_all_count_normalized'
                         ]]

        merged.to_csv(f'stimuli/word_features/word_features_{filename}.csv', sep='\t', index=False)


if __name__ == '__main__':
    # duplicate cols to check
    paths = [
        'stimuli/word_features',
    ]
    col1 = [
        'PoS_tag'

    ]
    col2 = [
        'STTS_PoS_tag'
    ]

    # rename_cols_all_files()

    #check_duplicate_cols(paths, col1, col2)

    # check_column_names_type()

    # check_col_vals()

    merge_text_tags_wf()
