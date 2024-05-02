from __future__ import annotations

import os

import numpy as np
import pandas as pd


def get_char_based_aoi_files() -> dict[str, pd.DataFrame]:
    char_based_aoi_df_dict = {}
    for text_type in ['b', 'p']:
        for text_id in range(6):
            text_name = f'{text_type}{text_id}'
            char_based_aoi_df_dict[text_name] = pd.read_csv(
                os.path.join(
                    'aoi_texts',
                    f'{text_name}.ias',
                ),
                delimiter='\t',
                keep_default_na=False,
                na_values=[
                    '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan',
                    '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a',
                    'nan', '',
                ],
            )

    return char_based_aoi_df_dict


def get_word_features_dict() -> dict[str, pd.DataFrame]:
    word_features_dict = {}
    for text_type in ['b', 'p']:
        for text_id in range(6):
            text_name = f'{text_type}{text_id}'
            word_features_dict[text_name] = pd.read_csv(
                os.path.join(
                    'word_features',
                    f'word_features_{text_name}.tsv',
                ),
                delimiter='\t',
                keep_default_na=False,
                na_values=[
                    '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan',
                    '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a',
                    'nan', '',
                ],
            )

    return word_features_dict


def create_word_aoi_df(
        char_based_aoi_dict: dict[str, pd.DataFrame],
        word_features_dict: dict[str, pd.DataFrame],
        text_name: str,
) -> pd.DataFrame:
    wf_text = word_features_dict[text_name]
    cb_aoi_text = char_based_aoi_dict[text_name]
    word_aoi_df = pd.DataFrame({col: [np.nan] * len(wf_text) for col in cb_aoi_text.columns})
    for _word_id, word_row in wf_text.iterrows():
        word_id = _word_id + 1
        lower_char_index, upper_char_index = eval(word_row['word_limit_char_indices'])
        upper_char_index += (len(word_row['word_with_punct']) - len(word_row['word']))
        tmp_word_aoi_df = cb_aoi_text.loc[cb_aoi_text['aoi'].isin(list(range(lower_char_index, upper_char_index+1)))].reset_index()
        word_aoi_df.at[_word_id, 'aoi_type'] = tmp_word_aoi_df['aoi_type'].iloc[0]
        word_aoi_df.at[_word_id, 'aoi'] = word_id
        word_aoi_df.at[_word_id, 'start_x'] = tmp_word_aoi_df['start_x'].iloc[0]
        word_aoi_df.at[_word_id, 'start_y'] = tmp_word_aoi_df['start_y'].iloc[0]
        word_aoi_df.at[_word_id, 'end_x'] = tmp_word_aoi_df['end_x'].iloc[-1]
        word_aoi_df.at[_word_id, 'end_y'] = tmp_word_aoi_df['end_y'].iloc[-1]
        word_aoi_df.at[_word_id, 'character'] = ''.join(tmp_word_aoi_df['character'].values)

    return word_aoi_df


def create_word_aoi_df_dict() -> dict[str, pd.DataFrame]:
    char_based_aoi_df_dict = get_char_based_aoi_files()
    word_features_dict = get_word_features_dict()
    word_aoi_df_dict = {}
    for text_type in ['b', 'p']:
        for text_id in range(6):
            text_name = f'{text_type}{text_id}'
            word_aoi_df = create_word_aoi_df(char_based_aoi_df_dict, word_features_dict, text_name)
            word_aoi_df_dict[text_name] = word_aoi_df

    return word_aoi_df_dict


def save_word_aoi_tsv() -> int:
    char_based_aoi_df_dict = get_char_based_aoi_files()
    word_features_dict = get_word_features_dict()
    word_aoi_texts_dir_name = 'word_aoi_texts'
    os.makedirs(word_aoi_texts_dir_name, exist_ok=True)
    for text_type in ['b', 'p']:
        for text_id in range(6):
            text_name = f'{text_type}{text_id}'
            word_aoi_df = create_word_aoi_df(char_based_aoi_df_dict, word_features_dict, text_name)
            word_aoi_df.to_csv(
                os.path.join(
                    word_aoi_texts_dir_name,
                    f'word_aoi_{text_name}.tsv',
                ),
                sep='\t',
                index=None,
            )

    return 0


def main() -> int:
    return save_word_aoi_tsv()


if __name__ == '__main__':
    raise SystemExit(main())
