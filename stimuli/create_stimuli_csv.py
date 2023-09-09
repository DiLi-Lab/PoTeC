import os
import re

import pandas as pd


def main():
    items = pd.read_csv('itemsEB.csv', sep='\t')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    cols = ['version', 'text_id', 'topic', 'text', 'headline', 'tq_1',
            'tq_1_option1', 'tq_1_option2', 'tq_1_option3', 'tq_1_option4', 'tq_2',
            'tq_2_option1', 'tq_2_option2', 'tq_2_option3', 'tq_2_option4', 'tq_3',
            'tq_3_option1', 'tq_3_option2', 'tq_3_option3', 'tq_3_option4', 'bq_1',
            'bq_1_option1', 'bq_1_option2', 'bq_1_option3', 'bq_1_option4', 'bq_2',
            'bq_2_option1', 'bq_2_option2', 'bq_2_option3', 'bq_2_option4', 'bq_3',
            'bq_3_option1', 'bq_3_option2', 'bq_3_option3', 'bq_3_option4',
            'order_bqs', 'order_tqs', 'order_bq_1_ans', 'order_bq_2_ans',
            'order_bq_3_ans', 'order_tq_1_ans', 'order_tq_2_ans', 'order_tq_3_ans',
            'correct_ans_tq_1', 'correct_ans_tq_2', 'correct_ans_tq_3',
            'correct_ans_bq_1', 'correct_ans_bq_2', 'correct_ans_bq_3', 'trial']
    items.columns = cols

    # read all the column values and replace the * by an empty string and then write the csv file again
    for col in cols:
        # check whether the column contains strings
        if items[col].dtype == 'object':
            # replace the * by an empty string
            items[col] = items[col].str.replace('*', '')

    items.to_csv('text_and_questions.tsv', sep='\t', index=False)


if __name__ == '__main__':
    main()
