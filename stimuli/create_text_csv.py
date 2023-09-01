import os

import pandas as pd

def main():
    inital_df = pd.read_csv('texts_and_questions/text_and_questions.csv')

    bio_path = 'texts_and_questions/bio_texts/'
    physics_path = 'texts_and_questions/physics_texts/'

    bio_files = os.listdir(bio_path)
    physics_files = os.listdir(physics_path)

    d = {c: [] for c in inital_df.columns}

    gen = ['title', 'text', 'tq_1', 'tq_1_option_1', 'tq_1_option_2', 'tq_1_option_3', 'tq_1_option_4', 't1_2',
           'tq_2_option_1', 'tq_2_option_2', 'tq_2_option_3', 'tq_2_option_4', 'tq_3', 'tq_3_option_1',
           'tq_3_option_2', 'tq_3_option_3', 'tq_3_option_4', 'bq_1', 'bq_1_option_1', 'bq_1_option_2',
           'bq_1_option_3', 'bq_1_option_4', 'b1_2', 'bq_2_option_1', 'bq_2_option_2', 'bq_2_option_3',
           'bq_2_option_4', 'bq_3', 'bq_3_option_1', 'bq_3_option_2', 'bq_3_option_3', 'bq_3_option_4', 'source',
           ]

    for path in bio_files:
        with open(bio_path + path, 'r') as f:
            gen_z = (c for c in gen)
            for idx, line in enumerate(f.readlines()):
                if idx in [2, 3, 4, 30, 37]:
                    continue
                elif idx == 36:
                    line = line.replace('Quelle: ', '')
                    d[next(gen_z)].append(line.strip())
                else:
                    d[next(gen_z)].append(line.strip())

            d['id'].append(path.split('.')[0])


    # do same for physics
    for path in physics_files:
        with open(physics_path + path, 'r') as f:
            gen_z = (c for c in gen)
            for idx, line in enumerate(f.readlines()):
                if idx in [2, 3, 4, 30, 37]:
                    continue
                elif idx == 36:
                    line = line.replace('Quelle: ', '')
                    d[next(gen_z)].append(line.strip())
                else:
                    d[next(gen_z)].append(line.strip())

            # add title from path name
            d['id'].append(path.split('.')[0])

    df = pd.DataFrame(d)
    df.sort_values('id', inplace=True)
    df.to_csv('texts_and_questions/text_and_questions.csv', index=False)


if __name__ == '__main__':
    main()