#!/usr/bin/env python3
"""
Computes reading measures based on fixation data
Call: python3 compute_reading_measures.py
"""

import argparse
import json
import logging
import os
import statistics
from pathlib import Path

import pandas as pd
from tqdm import tqdm

logging.basicConfig(filename='rm_error_log.txt', level=logging.ERROR)

FIX_INDEX_COL_NAME = 'CURRENT_FIX_INDEX'
FIX_DUR_COL_NAME = 'CURRENT_FIX_DURATION'
ROI_COL_NAME = 'roi'
DELIMITER = '\s+'


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
        fixation_folder: str,
        output_folder: str,
        participants_file: str,
        word_limits_json: str,
        sent_limits_json: str,
) -> None:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # read all the files we need
    fixation_filenames = list(Path(fixation_folder).glob('*.txt'))
    df_participants = pd.read_csv(participants_file, delimiter=",")

    with open(word_limits_json, 'r') as limits_w_json:
        word_limits = json.load(limits_w_json)

    with open(sent_limits_json, 'r') as limits_s_json:
        sent_limits = json.load(limits_s_json)

    for fixation_file_path in tqdm(fixation_filenames):
        reader, text_id, _ = Path(fixation_file_path).stem.split("_")
        word_limits_text = word_limits[text_id]
        sent_limits_text = sent_limits[text_id]

        output_file_name = reader + '_' + text_id + '_rm.csv'
        output_file_name = os.path.join(output_folder, output_file_name)

        # reader is always reader[number], we need to extract actual id
        reader_id = int(reader[6:])

        # select participant's row
        reader_row = df_participants.loc[df_participants['readerId'] == reader_id]

        # get participant information
        major = reader_row['major'].item()
        gender = reader_row['gender'].item()
        expert_status = reader_row['beginner/expert'].item()
        age = reader_row['age'].item()

        fixation_file = pd.read_csv(fixation_file_path, delimiter=DELIMITER)

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
                'WordIndexSent': word_index - sent_limits_text[0][(roi2word(word_index, sent_limits_text)) - 1] + 1,
                'SentIndex': roi2word(word_index, sent_limits_text), 'FFD': 0, 'SFD': 0, 'FD': 0, 'FPRT': 0,
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
            acc_tq1, acc_tq2, acc_tq3 = fixation_file_sorted[['ACC_T_Q1', 'ACC_T_Q2', 'ACC_T_Q3']].mean()
            acc_bq1, acc_bq2, acc_bq3 = fixation_file_sorted[['ACC_B_Q1', 'ACC_B_Q2', 'ACC_B_Q3']].mean()

            mean_acc_tq = statistics.mean([acc_bq1, acc_bq2, acc_bq3])
            mean_acc_bq = statistics.mean([acc_tq1, acc_tq2, acc_tq3])

        except ValueError:
            # if no accuracy information is available, code with -1
            acc_tq1 = acc_tq2 = acc_tq3 = acc_bq1 = acc_bq2 = acc_bq3 = mean_acc_tq = mean_acc_bq = -1
            # print(f'No accuracy values for {fixation_file_path}')
            logging.error("No accuracy values for", str(fixation_file_path),  exc_info=True)

        except TypeError:
            # if no accuracy information is available, code with -1
            acc_tq1 = acc_tq2 = acc_tq3 = acc_bq1 = acc_bq2 = acc_bq3 = mean_acc_tq = mean_acc_bq = -1
            # print(f'No accuracy values for {fixation_file_path}')
            logging.error("No accuracy values for", str(fixation_file_path),  exc_info=True)

        topic = 1 if fixation_file_sorted.loc[1, 'topic'] == 'bio' else -1  # Coding of topic: bio=1, phy=-1
        trial = fixation_file_sorted.loc[1, 'trial']
        itemid = fixation_file_sorted.loc[1, 'itemid']
        gender = 1 if gender == "w" else -1  # Coding of gender: f=1, m=-1
        major = 1 if major == "B" else -1  # Coding of major: B=1, P=-1
        expert_status = 1 if expert_status == 'E' else -1  # Coding of expert_status: E=1, A=-1

        # Add group column: Bio/Beginner=1, Bio/Expert=2, Physics/Beginner=3, Physics/Expert=4
        if major == "B":
            if expert_status == "A":
                group = 1
            else:
                group = 2
        else:
            if expert_status == "A":
                group = 3
            else:
                group = 4

        trial_information_header = [
            'ACC_B_Q1', 'ACC_B_Q2', 'ACC_B_Q3', 'ACC_T_Q1', 'ACC_T_Q2', 'ACC_T_Q3', 'topic',
            'trial', 'itemid', 'reader', 'gender', 'major', 'expert_status', 'age',
            'meanAccBQ', 'meanAccTQ', 'group'
        ]

        trial_information = [
            acc_bq1, acc_bq2, acc_bq3, acc_tq1, acc_tq2, acc_tq3, topic, trial, itemid, reader_id, gender, major,
            expert_status, age, mean_acc_bq, mean_acc_tq, group
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
        rm_reader_text_pair_df.to_csv(output_file_name, index=False, sep='\t')


def create_parser():
    base_path = Path(os.getcwd()).parent
    pars = argparse.ArgumentParser()

    pars.add_argument(
        '--fixation-folder',
        default=base_path / 'eyetracking_data/fixations',
    )

    pars.add_argument(
        '--participants-file',
        default=base_path / 'participants/participant_data.csv',
    )

    pars.add_argument(
        '--word-limits-json',
        default=base_path / 'preprocessing_scripts/word_limits.json',
    )

    pars.add_argument(
        '--sent-limits-json',
        default=base_path / 'preprocessing_scripts/sent_limits.json',
    )

    pars.add_argument(
        '--output-folder',
        default=base_path / 'eyetracking_data/reading_measures',
    )

    return pars


if __name__ == '__main__':
    parser = create_parser()
    args = vars(parser.parse_args())

    compute_reading_measures(**args)
