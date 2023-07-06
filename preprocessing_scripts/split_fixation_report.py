# This code splits the Fixation Report created by data viewer into separate files, one file per reader and text. In
# addition, it creates a file containing all reader IDs (RECORDING_SESSION_LABEL) FixRep darf wegen encoding keine
# interest area labels beinhalten
import argparse
import csv
import os
from pathlib import Path

import pandas as pd
from tqdm import tqdm


# Aufruf: python3 split_fixation_report.py ../data/<filename Fixation Report> <filename fixrep outputfiles>


def split_fixation_report(
        fixation_report_file: str,
        reader_ids_file: str,
        output_folder: str,
        columns: list,
) -> None:
    fix_rep_csv = pd.read_csv(fixation_report_file, sep='\t', iterator=True, chunksize=5000, index_col=False)
    header = []
    reader_ids = set()  # save readerIds to write into a separate file (for later use)

    reader_ids_item_ids = set()  # set to store all already seen reader and itemids (used below to first write col names
    # when a text read by a reader is encountered for the first time

    output_file_name = ''
    reader_item_df = pd.DataFrame()

    for chunk in fix_rep_csv:
        if not header:
            header = chunk.columns.values.tolist()
            reader_item_df = pd.DataFrame(columns=header)

        for index, row in tqdm(chunk.iterrows(), total=5000, desc='Splitting report: '):

            reader_id = str(row['RECORDING_SESSION_LABEL'])
            item_id = row['itemid']
            reader_item = str(reader_id) + item_id  # combination of reader and itemid

            if reader_item not in reader_ids_item_ids:
                # dump last reader-item df to file unless it is the first reader and item
                if not reader_item_df.empty:
                    reader_item_df = reader_item_df[columns]
                    reader_item_df.rename(
                        columns={'CURRENT_FIX_INTEREST_AREA_INDEX': 'roi', 'RECORDING_SESSION_LABEL': 'readerID'},
                        inplace=True,
                    )
                    reader_item_df.to_csv(output_file_name, sep='\t', index=False)

                reader_item_df = pd.DataFrame(columns=header)
                output_file_name = Path(output_folder) / ('reader' + reader_id + '_' + item_id + '_FIX.csv')
                reader_ids.add(reader_id)  # save readerId if encountered for the first time
                reader_ids_item_ids.add(reader_item)  # save reader-item combination if encountered for the first time

            reader_item_df = reader_item_df.append(row, ignore_index=False)

    reader_item_df.to_csv(output_file_name, sep='\t', index=False, header=header)

    reader_file = open(reader_ids_file, 'w')  # create file to save reader ids

    writer = csv.writer(reader_file, delimiter='\t', lineterminator='\n')
    writer.writerow(reader_ids)
    reader_file.close()


def create_parser():
    base_path = Path(os.getcwd()).parent
    pars = argparse.ArgumentParser()

    pars.add_argument(
        '-fp', '--fixation-report-file',
        default=base_path / 'eyetracking_data/FixRep_20_Mai_2017.txt',
    )

    pars.add_argument(
        '-rid', '--reader-ids-file',
        default=base_path / 'participants/ReaderIDs.txt',
    )

    pars.add_argument(
        '-c', '--columns',
        default=['CURRENT_FIX_INDEX', 'topic', 'trial', 'ACC_B_Q1', 'ACC_B_Q2', 'ACC_B_Q3', 'ACC_T_Q1', 'ACC_T_Q2',
                 'ACC_T_Q3', 'CURRENT_FIX_DURATION', 'NEXT_SAC_DURATION', 'PREVIOUS_SAC_DURATION', 'version',
                 'CURRENT_FIX_INTEREST_AREA_INDEX', 'RECORDING_SESSION_LABEL', 'itemid'],
    )

    pars.add_argument(
        '-o', '--output-folder',
        default=base_path / 'eyetracking_data/fixations/',
    )

    pars.add_argument(
        '-ow', '--overwrite',
        action='store_true',
    )

    return pars


if __name__ == '__main__':
    parser = create_parser()
    args = vars(parser.parse_args())

    if os.listdir(args['output_folder']) and not args['overwrite']:
        raise ValueError("The output folder is not empty! If you want to overwrite any files please specify by "
                         "explicitly adding the overwrite flag.")

    args.pop('overwrite')

    split_fixation_report(**args)
