import re
from pathlib import Path

import numpy as np
import pandas as pd
import tqdm


def get_validation_scores(path):
    validation_regex = r'MSG.+VALIDATION\s+HV(?P<num_points>\d\d?).*(?P<eye_tracked>LEFT|RIGHT).*(?P<validation_score_avg>\d.\d\d)\s+avg\.\s+(?P<validation_score_max>\d.\d\d)\s+max'
    calibration_regex = r'>>>>>>>\s+CALIBRATION\s+\(HV(?P<num_points>\d\d?),(?P<type>.*)\).*(?P<tracked_eye>RIGHT|LEFT):'

    files = Path(path).glob('*.asc')
    reader_ids = []
    validation_scores_avg = []
    validation_scores_max = []
    validation_lines = []
    calibration_lines = []
    num_points = []
    msg_type = []
    eye_tracked = []

    for file in tqdm.tqdm(files):

        reader_id = file.stem.split('_')[0]

        with open(file, 'r', encoding='utf8') as file:
            for line in file.readlines():
                if match := re.match(validation_regex, line):
                    validation_lines.append(line)
                    if reader_id == '21':
                        reader_id = '0'
                    reader_ids.append(reader_id)
                    d = match.groupdict()

                    validation_scores_avg.append(float(d['validation_score_avg']))
                    validation_scores_max.append(float(d['validation_score_max']))
                    num_points.append(d['num_points'])
                    msg_type.append('validation')
                    eye_tracked.append(d['eye_tracked'])
                    calibration_lines.append('')

                if match := re.match(calibration_regex, line):
                    d = match.groupdict()
                    num_points.append(d['num_points'])
                    if reader_id == '21':
                        reader_id = '0'
                    reader_ids.append(reader_id)
                    calibration_lines.append(line)
                    eye_tracked.append(d['tracked_eye'])
                    msg_type.append('calibration')
                    validation_lines.append('')
                    validation_scores_avg.append(-1)
                    validation_scores_max.append(-1)

    df = pd.DataFrame({'reader_id': reader_ids, 'validation_score_avg': validation_scores_avg,
                       'validation_score_max': validation_scores_max, 'num_points': num_points,
                       'validation_lines': validation_lines, 'calibration_lines': calibration_lines,
                       'type': msg_type, 'eye_tracked': eye_tracked})
    grouped_df = df.groupby(['reader_id', 'type', 'eye_tracked', 'num_points'])
    final_df = grouped_df.agg({
        'validation_score_avg': 'mean',
        'validation_score_max': 'mean',
    }).reset_index()

    final_df['count'] = grouped_df.size().reset_index()[0]
    final_df = final_df.round(3)
    final_df = final_df.replace(-1, pd.NA)

    final_df.sort_values(by='reader_id')

    final_df.rename(columns={'calibration_lines': 'num_calibration', 'validation_lines': 'num_validation'}, inplace=True)
    final_df.to_csv('validation_scores.csv', index=False)

    # new = final_df[final_df['type'] == 'validation']
    # new.astype({'validation_score_avg': 'float64', 'validation_score_max': 'float64', 'count': 'int64'})

    overall_df = final_df.groupby(['type'])[['count', 'validation_score_max', 'validation_score_avg']].agg(['mean', 'max', 'min']).reset_index()
    overall_df = overall_df.round(3)
    overall_df.to_csv('overall_validation_scores.csv', index=False)


if __name__ == "__main__":
    get_validation_scores('/eyetracking_data/asc_files')
