from pathlib import Path

import pandas as pd

PATHS_FOLDERS = [
    '../stimuli/stimuli/items.tsv',
    '../stimuli/stimuli/stimuli.tsv',
    '../stimuli/aoi_texts/',
    '../stimuli/word_features/',
    '../participants/',
    '../eyetracking_data/fixations/',
    '../eyetracking_data/reading_measures/',
    '../eyetracking_data/reader_rm_wf/',
    '../eyetracking_data/scanpaths/',
    '../eyetracking_data/scanpaths_reader_rm_wf/',
    '../preprocessing_scripts/roi_to_word.tsv',
]

text_vars = [
    'text',
    'headline',
    'bq_1',
    'bq_1_option1',
    'bq_1_option2',
    'bq_1_option3',
    'bq_1_option4',
    'bq_2',
    'bq_2_option1',
    'bq_2_option2',
    'bq_2_option3',
    'bq_2_option4',
    'bq_3',
    'bq_3_option1',
    'bq_3_option2',
    'bq_3_option3',
    'bq_3_option4',
    'tq_1',
    'tq_1_option1',
    'tq_1_option2',
    'tq_1_option3',
    'tq_1_option4',
    'tq_2',
    'tq_2_option1',
    'tq_2_option2',
    'tq_2_option3',
    'tq_2_option4',
    'tq_3',
    'tq_3_option1',
    'tq_3_option2',
    'tq_3_option3',
    'tq_3_option4',
    'character',
    'lemma',
    'syllables',
    'word',
    'type',
]
cat_vars = [
    'alcohol',
    'contains_abbreviation',
    'contains_hyphen',
    'contains_symbol',
    'domain_expert_status',
    'domain_expert_status_numeric',
    'expert_status',
    'expert_status_numeric',
    'is_abbreviation',
    'is_clause_beginning',
    'is_fixation_adjusted',
    'is_in_parentheses',
    'is_in_quote',
    'is_sent_beginning',
    'is_technical_term',
    'reader_domain',
    'reader_domain_numeric',
    'FPF',
    'FPReg',
    'Fix',
    'RR',
    'gender',
    'gender_numeric',
    'glasses',
    'handedness',
    'PoS_tag',
    'STTS_PoS_tag',
    'STTS_punctuation_after',
    'STTS_punctuation_before',
    'text_domain',
    'text_domain_numeric',

    'text_id',

]
cont_vars = [
    'annotated_type_frequency_normalized',
    'avg_cond_prob_in_bigrams',
    'avg_cond_prob_in_trigrams',
    'cumulative_character_bigram_corpus_frequency_normalized',
    'cumulative_character_bigram_lexicon_frequency_normalized',
    'cumulative_character_corpus_frequency_normalized',
    'cumulative_character_lexicon_frequency_normalized',
    'cumulative_character_trigram_corpus_frequency_normalized',
    'cumulative_character_trigram_lexicon_frequency_normalized',
    'cumulative_syllable_corpus_frequency_normalized',
    'cumulative_syllable_lexicon_frequency_normalized',
    'document_frequency_normalized',
    'familiarity_normalized',
    'neighbors_coltheart_all_count_normalized',
    'neighbors_coltheart_all_cum_freq_normalized',
    'neighbors_coltheart_higher_freq_count_normalized',
    'neighbors_coltheart_higher_freq_cum_freq_normalized',
    'neighbors_levenshtein_all_count_normalized',
    'neighbors_levenshtein_all_cum_freq_normalized',
    'neighbors_levenshtein_higher_freq_count_normalized',
    'neighbors_levenshtein_higher_freq_cum_freq_normalized',
    'FD',
    'FFD',
    'FPRT',
    'SFD',
    'TFT',
    'FRT',
    'RRT',
    'RPD_exc',
    'RPD_inc',
    'RBRT',
    'acc_bq_1',
    'acc_bq_2',
    'acc_bq_3',
    'acc_tq_1',
    'acc_tq_2',
    'acc_tq_3',
    'regularity_normalized',
    'initial_bigram_frequency_normalized',
    'initial_letter_frequency_normalized',
    'initial_trigram_frequency_normalized',
    'sentence_frequency_normalized',
    'lemma_frequency_normalized',
    'type_frequency_normalized',
    'age',
    'hours_sleep',

    'mean_acc_bq',
    'mean_acc_tq',
]
ints = [
    'SL_in',
    'SL_out',
    'LP',
    'TRC_in',
    'TRC_out',
    'word_length',
    'lemma_length_chars',
    'type_length_chars',
    'type_length_syllables',
    'line',
    'char_index_in_line',
    'char_index_in_text',
    'fixation_index',
    'word_index_in_sent',
    'word_index_in_text',
    'original_fixation_index',
    'trial',
    'roi',
    'sent_index_in_text',
    'reader_id',
    'version',
    'end_x',
    'end_y',
    'start_x',
    'start_y',
    'correct_ans_bq_1',
    'correct_ans_bq_2',
    'correct_ans_bq_3',
    'correct_ans_tq_1',
    'correct_ans_tq_2',
    'correct_ans_tq_3',
    'fixation_duration',
    'next_saccade_duration',
    'previous_saccade_duration',
]

no_stats = [
    'order_bq_1_ans',
    'order_bq_2_ans',
    'order_bq_3_ans',
    'order_tq_1_ans',
    'order_tq_2_ans',
    'order_tq_3_ans',
    'word_limit_char_indices',
]


def create_codebook_tables():

    all_cols = set()

    codebook_text = pd.read_csv('codebook_texts.tsv', sep='\t')

    with open('../CODEBOOK.md', 'w', encoding='utf8') as md_tables:
        codebook_header = (f'# Codebook\n'
                           f'The codebook specifies the data types, possible values, and other information '
                           f'for each column in the data files.\n\n')

        md_tables.write(codebook_header)

    for folder in PATHS_FOLDERS:
        # iterate over all tsv files in all folders

        cols = {}

        if folder.endswith('.tsv'):
            files = [folder]
        else:
            suffix = '.ias' if folder == '../stimuli/aoi_texts/' else '.tsv'
            files = Path(folder).glob(f'*{suffix}')

        for file in files:

            tsv = pd.read_csv(file, sep='\t', keep_default_na=False,
                              na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND',
                                         '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan', ''])

            all_cols.update(tsv.columns)

            for c in tsv.columns:
                try:
                    cols[c]['values'] = pd.concat([cols[c]['values'], tsv[c]], ignore_index=True)
                    cols[c]['dtypes'] += [tsv[c].dtype]
                except KeyError:
                    cols[c] = {'values': tsv[c]}
                    cols[c]['dtypes'] = [tsv[c].dtype]

        for col_name, col_dict in cols.items():
            col_dict['missing_values'] = col_dict['values'].isnull().sum().sum()

            if col_name in no_stats:
                col_dict['possible_values'] = 'no stats?'
                col_dict['value_type'] = pd.NA

            elif col_name in ['text_id']:
                col_dict['possible_values'] = ', '.join(sorted(list(set(col_dict['values']))))
                col_dict['value_type'] = ''

            elif col_name in cont_vars:
                col_dict['value_type'] = 'Float'
                col_dict[
                    'possible_values'] = f"min: {col_dict['values'].min()}, max: {col_dict['values'].max()}, mean: {col_dict['values'].mean()}, std: {col_dict['values'].std()}"

            elif col_name in cat_vars:
                counts = col_dict['values'].value_counts(dropna=False)
                col_dict['value_type'] = 'Categorical'

                count_str = ''
                for k, v in counts.to_dict().items():
                    count_str += f"{k}: {v}, "

                col_dict['possible_values'] = count_str[:-2]

            elif col_name in ints:
                col_dict['possible_values'] = f"{min(col_dict['values'])}-{max(col_dict['values'])}"
                col_dict['value_type'] = 'Integer'

            elif col_name in text_vars:
                col_dict['possible_values'] = ''
                col_dict['value_type'] = 'string'

            else:
                col_dict['possible_values'] = ''
                col_dict['value_type'] = pd.NA

        df_lists = {'Column name': [], 'Possible values': [], 'Value type': [], 'Description': [],
                    'Num missing values': [], 'Missing value description': [], 'Source': []}

        info_tsv = pd.read_csv('all_cols_description.tsv', sep='\t')

        for k, v in cols.items():
            df_lists['Column name'].append(k)
            df_lists['Possible values'].append(v['possible_values'])
            df_lists['Value type'].append(v['value_type'])
            df_lists['Num missing values'].append(f"{v['missing_values']}")
            df_lists['Missing value description'].append(
                info_tsv[info_tsv['Column_name'] == k]['Missing value description'].values[0]
            )
            df_lists['Description'].append(info_tsv[info_tsv['Column_name'] == k]['Description'].values[0])
            df_lists['Source'].append(info_tsv[info_tsv['Column_name'] == k]['Source'].values[0])

        df = pd.DataFrame(df_lists)
        df.to_csv(f'../codebook_tables/{Path(folder).stem}.tsv', sep='\t', index=False)

        with open('../CODEBOOK.md', 'a', encoding='utf8') as md_tables:
            title = codebook_text[codebook_text['section'] == folder[3:]]['title'].values[0]
            description = codebook_text[codebook_text['section'] == folder[3:]]['text'].values[0]
            link = codebook_text[codebook_text['section'] == folder[3:]]['link'].values[0]

            md = df.to_markdown(index=False)
            md_tables.write(f'## {title}\n')
            md_tables.write(f'{description}\n\n{link}\n\n')
            md_tables.write(md)

            md_tables.write('\n\n\n')


if __name__ == '__main__':
    create_codebook_tables()
