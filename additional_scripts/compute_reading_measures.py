#!/usr/bin/env python3
"""
Computes reading measures based on fixation data
Call: python3 compute_reading_measures.py
"""

import json
import os
import statistics
from pathlib import Path

import pandas as pd
from tqdm import tqdm


FIX_INDEX_COL_NAME = 'fixation_index'
FIX_DUR_COL_NAME = 'fixation_duration'
ROI_COL_NAME = 'roi'
DELIMITER = '\t'


def roi2word(roi: int, word_limits: list) -> int:
    """
    Creates mapping between roi and word index in text. Word_limits is a list of two lists, containing the first and
    the last roi of a word. Checks whether roi is in a word interval and returns the word index in the text (starting at 1).
    Returns a negative index if it is between two words.
    """
    for index, (word_start_roi, word_end_roi) in enumerate(zip(word_limits[0], word_limits[1])):
        if word_start_roi <= roi <= word_end_roi:
            return index + 1
        # if the roi is smaller than the start of the word and the end of the word but apparently also not in the word
        # before that word we know it is not in a word
        if roi < word_start_roi:
            return - index - 1
    return -1


def compute_reading_measures(
        fixation_folder: Path,
        output_folder: Path,
        participants_file: Path,
        word_limits_json: Path,
        sent_limits_json: Path,
        stimulus_overview: Path,
) -> None:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # read all the files we need
    fixation_filenames = list(Path(fixation_folder).glob('*.tsv'))
    df_participants = pd.read_csv(participants_file, delimiter="\t")
    stimuli = pd.read_csv(stimulus_overview, delimiter="\t")

    with open(word_limits_json, 'r') as limits_w_json:
        word_limits = json.load(limits_w_json)

    with open(sent_limits_json, 'r') as limits_s_json:
        sent_limits = json.load(limits_s_json)

    for fixation_file_path in tqdm(fixation_filenames):
        reader, text_id, _ = Path(fixation_file_path).stem.split("_")
        word_limits_text = word_limits[text_id]
        sent_limits_text = sent_limits[text_id]

        text_id_numeric = stimuli.loc[stimuli['text_id'] == text_id, 'text_id_numeric'].item()

        output_file_name = reader + '_' + text_id + '_rm.tsv'
        output_file_name = os.path.join(output_folder, output_file_name)

        # reader is always reader[number], we need to extract actual id
        reader_id = int(reader[6:])

        # select participant's row
        reader_row = df_participants.loc[df_participants['reader_id'] == reader_id]

        # get participant information
        reader_domain_numeric = reader_row['reader_domain_numeric'].item()
        gender_numeric = reader_row['gender_numeric'].item()
        expert_status_numeric = reader_row['expert_status_numeric'].item()
        domain_expert_status_numeric = reader_row['domain_expert_status_numeric'].item()
        age = reader_row['age'].item()

        fixation_file = pd.read_csv(fixation_file_path, delimiter=DELIMITER, keep_default_na=False,
                                    na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan',
                                               '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a',
                                               'nan', ''])

        # make sure fixations are sorted by their index
        fixation_file_sorted = fixation_file.sort_values(by=[FIX_INDEX_COL_NAME])

        # append one extra dummy fixation to have a next fixation for the actual last fixation
        pd.concat(
            [fixation_file_sorted,
             pd.DataFrame(
                 [[0 for _ in range(len(fixation_file_sorted.columns))]], columns=fixation_file_sorted.columns
             )],
            ignore_index=True,
        )

        # iterate over words in that text
        word_dict = {}
        num_words_in_text = len(word_limits_text[0])

        for word_index in range(1, num_words_in_text + 1):
            word_row = {
                'word_index_in_sent': word_index - sent_limits_text[0][
                    (roi2word(word_index, sent_limits_text)) - 1] + 1,
                'sent_index_in_text': roi2word(word_index, sent_limits_text), 'FFD': 0, 'SFD': 0, 'FD': 0, 'FPRT': 0,
                'FRT': 0, 'TFT': 0, 'RRT': 0, 'RPD_inc': 0, 'RPD_exc': 0, 'RBRT': 0, 'Fix': 0,
                'FPF': 0, 'RR': 0, 'FPReg': 0, 'TRC_out': 0, 'TRC_in': 0, 'LP': 0, 'SL_in': 0, 'SL_out': 0
            }

            word_dict[word_index] = word_row

        right_most_word = cur_fix_word_idx = next_fix_word_idx = next_fix_dur = 0

        for index, fixation in fixation_file_sorted.iterrows():

            roi = fixation[ROI_COL_NAME]

            # If roi is not a number (i.e., coded as missing value using any string), continue
            try:
                int(roi)
            except ValueError:
                continue

            # if fixation is not on a word, continue
            word_idx = roi2word(roi, word_limits_text)
            if word_idx < 0:
                continue

            last_fix_word_idx = cur_fix_word_idx

            cur_fix_word_idx = next_fix_word_idx
            cur_fix_dur = next_fix_dur

            next_fix_word_idx = word_idx
            next_fix_dur = fixation[FIX_DUR_COL_NAME]

            if next_fix_dur == "0":
                # we set the idx to the idx of the actual last fixation s.t. there is no error later in the script
                next_fix_word_idx = cur_fix_word_idx

            if word_dict[next_fix_word_idx]['LP'] == 0:
                word_dict[next_fix_word_idx]['LP'] = int(roi) - word_limits_text[0][next_fix_word_idx - 1] + 1
            if right_most_word < cur_fix_word_idx:
                right_most_word = cur_fix_word_idx

            if cur_fix_word_idx == 0:
                continue

            word_dict[cur_fix_word_idx]['TFT'] += int(cur_fix_dur)

            if word_dict[cur_fix_word_idx]['FD'] == 0:
                word_dict[cur_fix_word_idx]['FD'] += int(cur_fix_dur)

            if right_most_word == cur_fix_word_idx:
                if word_dict[cur_fix_word_idx]['TRC_out'] == 0:
                    word_dict[cur_fix_word_idx]['FPRT'] += int(cur_fix_dur)
                    if last_fix_word_idx < cur_fix_word_idx:
                        word_dict[cur_fix_word_idx]['FFD'] += int(cur_fix_dur)
            else:
                if right_most_word < cur_fix_word_idx:
                    print('error')
                word_dict[right_most_word]['RPD_exc'] += int(cur_fix_dur)

            if cur_fix_word_idx < last_fix_word_idx:
                word_dict[cur_fix_word_idx]['TRC_in'] += 1
            if cur_fix_word_idx > next_fix_word_idx:
                word_dict[cur_fix_word_idx]['TRC_out'] += 1
            if cur_fix_word_idx == right_most_word:
                word_dict[cur_fix_word_idx]['RBRT'] += int(cur_fix_dur)
            if word_dict[cur_fix_word_idx]['FRT'] == 0 and (
                    not next_fix_word_idx == cur_fix_word_idx or next_fix_dur == "0"):
                word_dict[cur_fix_word_idx]['FRT'] = word_dict[cur_fix_word_idx]['TFT']
            if word_dict[cur_fix_word_idx]['SL_in'] == 0:
                word_dict[cur_fix_word_idx]['SL_in'] = cur_fix_word_idx - last_fix_word_idx
            if word_dict[cur_fix_word_idx]['SL_out'] == 0:
                word_dict[cur_fix_word_idx]['SL_out'] = next_fix_word_idx - cur_fix_word_idx

        try:
            acc_tq1, acc_tq2, acc_tq3 = fixation_file_sorted[['acc_tq_1', 'acc_tq_2', 'acc_tq_3']].mean()
            acc_bq1, acc_bq2, acc_bq3 = fixation_file_sorted[['acc_bq_1', 'acc_bq_2', 'acc_bq_3']].mean()

            mean_acc_tq = statistics.mean([acc_bq1, acc_bq2, acc_bq3])
            mean_acc_bq = statistics.mean([acc_tq1, acc_tq2, acc_tq3])

        except (ValueError, TypeError):
            # if no accuracy information is available, code with -1
            acc_tq1 = acc_tq2 = acc_tq3 = acc_bq1 = acc_bq2 = acc_bq3 = mean_acc_tq = mean_acc_bq = pd.NA

        # Coding of topic: bio=1, phy=0
        if fixation_file_sorted.loc[1, 'text_domain'] == 'bio':
            text_domain_numeric = 1
        elif fixation_file_sorted.loc[1, 'text_domain'] == 'physics':
            text_domain_numeric = 0
        else:
            text_domain_numeric = pd.NA

        trial = fixation_file_sorted.loc[1, 'trial']
        text_id = fixation_file_sorted.loc[1, 'text_id']

        trial_information_header = [
            'text_domain_numeric',
            'trial', 'text_id', 'text_id_numeric', 'reader_id', 'gender_numeric', 'reader_domain_numeric', 'expert_status_numeric',
            'domain_expert_status_numeric', 'age',
            'mean_acc_bq', 'mean_acc_tq', 'acc_bq_1', 'acc_bq_2', 'acc_bq_3', 'acc_tq_1', 'acc_tq_2', 'acc_tq_3',
        ]

        trial_information = [
            text_domain_numeric, trial, text_id, text_id_numeric, reader_id, gender_numeric, reader_domain_numeric,
            expert_status_numeric, domain_expert_status_numeric, age, mean_acc_bq, mean_acc_tq,
            acc_bq1, acc_bq2, acc_bq3, acc_tq1, acc_tq2, acc_tq3,
        ]

        for word_indices, word_rm in sorted(word_dict.items()):
            # calculate all remaining reading measures from the ones we just computed
            if word_rm['FFD'] == word_rm['FPRT']:
                word_rm['SFD'] = word_rm['FFD']
            word_rm['RRT'] = word_rm['TFT'] - word_rm['FPRT']
            word_rm['FPF'] = int(word_rm['FFD'] > 0)
            word_rm['RR'] = int(word_rm['RRT'] > 0)
            word_rm['FPReg'] = int(word_rm['RPD_exc'] > 0)
            word_rm['Fix'] = int(word_rm['TFT'] > 0)
            word_rm['RPD_inc'] = word_rm['RPD_exc'] + word_rm['RBRT']

            # if it is the first word, we create the df
            if word_indices == 1:
                rm_reader_text_pair_df = pd.DataFrame([word_rm])
            else:
                rm_reader_text_pair_df = pd.concat([rm_reader_text_pair_df, pd.DataFrame([word_rm])])

        trial_info_dict = {k: [v for _ in range(num_words_in_text)] for k, v in
                           zip(trial_information_header, trial_information)}

        rm_reader_text_pair_df = rm_reader_text_pair_df.join(pd.DataFrame(trial_info_dict))

        rm_reader_text_pair_df.fillna('NA', inplace=True)
        rm_reader_text_pair_df.to_csv(output_file_name, index=False, sep='\t')


def main() -> int:
    repo_root = Path(__file__).parent.parent

    sent_limits = repo_root / 'preprocessing_scripts/sent_limits.json'
    word_limits = repo_root / 'preprocessing_scripts/word_limits.json'
    participants = repo_root / 'participants/participant_data.tsv'
    fixation_folder = repo_root / 'eyetracking_data/fixations'
    stimulus_overview = repo_root / 'stimuli/stimuli/stimuli.tsv'
    output_folder = repo_root / 'eyetracking_data/reading_measures'

    compute_reading_measures(
        fixation_folder=fixation_folder,
        output_folder=output_folder,
        participants_file=participants,
        sent_limits_json=sent_limits,
        word_limits_json=word_limits,
        stimulus_overview=stimulus_overview,
    )

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
