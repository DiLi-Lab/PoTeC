import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import ttest_ind


def calculate_accuracy(data_file: str, answer_coding_file: str, output_file: str) -> None:
    # create a dict with the correct answers as numbers from the answer coding file
    answer_coding_csv = pd.read_csv(answer_coding_file, delimiter=",", index_col='VAR', encoding='utf-8')
    # filter only those rows where 'CORRECT_ANSWER' is True
    answer_coding_csv = answer_coding_csv[answer_coding_csv['CORRECT_ANSWER'] == True]

    answer_coding_dict = answer_coding_csv.to_dict('index')

    # read the data file
    data_csv = pd.read_csv(data_file, delimiter=",", encoding='utf-8')

    participant_ids = []
    text_ids = []
    text_domains = []
    acc_tq1s = []
    acc_tq2s = []
    acc_tq3s = []
    mean_accs = []
    reader_disciplines = []
    level_of_studies = []

    for index, row in data_csv.iterrows():
        # only consider native German speakers
        is_native_lang_german = row['PQ01']
        if not is_native_lang_german:
            continue

        # only consider those where all attention checks were answered correctly
        attention_checks = ['AA0' + str(i) for i in range(1, 7)]
        num_correct_attention_checks = 0
        num_trials = 12
        for ac in attention_checks:
            answer = row[ac]
            correct_answer = answer_coding_dict[ac]['RESPONSE']
            if answer == correct_answer:
                num_correct_attention_checks += 1

        is_biology = row['PQ03']
        is_physics = row['PQ04']

        if num_correct_attention_checks != 6:
            print(f'Participant {row["CASE"]} did not answer all attention checks correctly.')
            continue

        if is_biology == 1 and is_physics == 1:
            print(f'Participant {row["CASE"]} is both a biologist and a physicist.')
            continue

            # text_ids.append(ac)
            # text_domains.append('attention_check')
            # if answer == correct_answer:
            # mean_accs.append(1)
            # else:
            # mean_accs.append(0)

            # acc_tq1s.append(pd.NA)
            # acc_tq2s.append(pd.NA)
            # acc_tq3s.append(pd.NA)
            # num_trials = 18

        participant_ids.extend([row['CASE'] for _ in range(num_trials)])

        if is_biology == 1 and is_physics == 2:
            reader_disciplines.extend(['biology' for _ in range(num_trials)])
            level_of_studies.extend(['graduate' for _ in range(num_trials)])
        elif is_physics == 1 and is_biology == 2:
            reader_disciplines.extend(['physics' for _ in range(num_trials)])
            level_of_studies.extend(['graduate' for _ in range(num_trials)])
        else:
            reader_disciplines.extend(['unknown' for _ in range(num_trials)])
            level_of_studies.extend(['unknown' for _ in range(num_trials)])

        all_texts = ['B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'P0', 'P1', 'P2', 'P3', 'P4', 'P5']

        for text_id in all_texts:
            text_ids.append(str(text_id.lower()))
            text_domains.append('biology' if text_id[0] == 'B' else 'physics')
            for question in range(1, 4):
                column_name = f'{text_id}0{question}'
                answer = row[column_name]
                correct_answer = answer_coding_dict[column_name]['RESPONSE']
                if answer == correct_answer:
                    if question == 1:
                        acc_tq1s.append(1)
                    elif question == 2:
                        acc_tq2s.append(1)
                    elif question == 3:
                        acc_tq3s.append(1)
                else:
                    if question == 1:
                        acc_tq1s.append(0)
                    elif question == 2:
                        acc_tq2s.append(0)
                    elif question == 3:
                        acc_tq3s.append(0)

            mean_accs.append((acc_tq1s[-1] + acc_tq2s[-1] + acc_tq3s[-1]) / 3)

    accuracy_df = pd.DataFrame({
        'participant_id': participant_ids,
        'text_id': text_ids,
        'text_domain': text_domains,
        'acc_tq1': acc_tq1s,
        'acc_tq2': acc_tq2s,
        'acc_tq3': acc_tq3s,
        'mean_acc_tq': mean_accs,
        'reader_discipline': reader_disciplines,
        'level_of_studies': level_of_studies,
    })

    print(f'Total number of participants: {accuracy_df["participant_id"].nunique()}')

    accuracy_df.to_csv(output_file, index=False)

    overview = accuracy_df.groupby(['reader_discipline', 'level_of_studies', 'text_domain']).agg(
        mean_accuracy=('mean_acc_tq', 'mean'),
        std=('mean_acc_tq', 'std'),
        n_participants=('participant_id', 'nunique'),
    ).round(2)

    # print all pd df cols
    pd.set_option('display.max_columns', None)
    print(overview)


def compare_online_survey(online_data: str, accuracy_data_exp: str):
    online_accuracies = pd.read_csv(online_data, delimiter=",", encoding='utf-8')
    exp_accuracies = pd.read_csv(accuracy_data_exp, delimiter="\t", encoding='utf-8')


    for domain in ['biology', 'physics']:
        for discipline in ['biology', 'physics']:
            exp_subset = exp_accuracies[
                (exp_accuracies['reader_discipline'] == discipline) &
                (exp_accuracies['level_of_studies'] == 'graduate') &
                (exp_accuracies['text_domain'] == domain)]
            online_subset = online_accuracies[
                (online_accuracies['reader_discipline'] == discipline) &
                (online_accuracies['level_of_studies'] == 'graduate') &
                (online_accuracies['text_domain'] == domain)]

            # get mean accuracies for the tq questions for both subsets
            exp_mean_acc = exp_subset['mean_acc_tq'].dropna()
            online_mean_acc = online_subset['mean_acc_tq'].dropna()

            # perform t-test
            t_stat, p_val = ttest_ind(exp_mean_acc, online_mean_acc, equal_var=False)
            p_text = 'significant' if p_val <= 0.001 else 'not significant'
            if p_val <= 0.001:
                p_val_text = f'p <= 0.001'
            else:
                p_val_text = f'{round(p_val, 2)}'
            print(f'T-test for {domain} texts and {discipline} readers: {p_val_text}. It is {p_text}.\n')


if __name__ == '__main__':
    this_repo_path = str(Path(__file__).parent.parent.parent)

    parser = argparse.ArgumentParser()
    parser.add_argument('--data-file', type=str,
                        default=f'{this_repo_path}/participants/response_data_online_survey.csv')
    parser.add_argument('--answer-coding-file', type=str,
                        default=f'{this_repo_path}/participants/answer_coding_online_survey.csv')
    parser.add_argument('--output-file', type=str,
                        default=f'{this_repo_path}/participants/response_accuracy_online_survey.csv')

    parser.add_argument('--acc-exp', type=str,
                        default=f'{this_repo_path}/participants/participant_response_accuracy.tsv')
    args = parser.parse_args()

    calculate_accuracy(args.data_file, args.answer_coding_file, args.output_file)

    compare_online_survey(args.output_file, args.acc_exp)
