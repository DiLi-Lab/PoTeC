import os
from collections import Counter
from pathlib import Path

import pandas as pd
from tqdm import tqdm


def merge_fixations_and_coordinates() -> None:
    """
    Merge the fixations and the coordinates of the original fixations
    Returns
    -------

    """
    repo_root = Path(__file__).parent.parent

    uncorrected_fixations_folder = repo_root / 'eyetracking_data/fixations_uncorrected/'
    corrected_fixations_folder = repo_root / 'eyetracking_data/fixations/'
    output_folder = repo_root / 'eyetracking_data/merged_fixations_and_coordinates_uncorrected/'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fixation_paths = list(corrected_fixations_folder.glob('*.tsv'))

    reader_counts = Counter()

    for file in tqdm(fixation_paths, desc='Merging fixations and coordinates: ', total=len(fixation_paths)):
        file_name = file.stem
        uncorrected_file_name = f'{file_name.split("_")[0]}_{file_name.split("_")[1]}_uncorrected_fixations.tsv'
        reader_id = file_name.split('_')[0]
        text_id = file_name.split('_')[1]
        reader_counts.update([reader_id])
        uncorrected_fixations_file = uncorrected_fixations_folder / uncorrected_file_name

        df = pd.read_csv(file, sep='\t', index_col=False)
        df_uncorrected = pd.read_csv(uncorrected_fixations_file, sep='\t', index_col=False)

        aoi_df = pd.read_csv(repo_root / f'stimuli/aoi_texts/{text_id}.ias', sep='\t', index_col=False)

        # if the fixation in the corrected fixation df was corrected we take the center of the aoi char box
        for index, row in df.iterrows():
            if row['is_fixation_adjusted']:
                roi = row['roi']

                # get the coordinates of the roi from the aoi_df
                try:
                    start_x = aoi_df.loc[aoi_df['roi'] == roi, 'start_x'].values[0]
                    start_y = aoi_df.loc[aoi_df['roi'] == roi, 'start_y'].values[0]
                    end_x = aoi_df.loc[aoi_df['roi'] == roi, 'end_x'].values[0]
                    end_y = aoi_df.loc[aoi_df['roi'] == roi, 'end_y'].values[0]

                    # calculate the center of the roi
                    new_x, new_y = (start_x + end_x) / 2, (start_y + end_y) / 2

                    df.at[index, 'fixation_position_x'] = new_x
                    df.at[index, 'fixation_position_y'] = new_y
                except IndexError:
                    print(file_name, roi, index)

            else:
                new_x = df_uncorrected.loc[df_uncorrected['fixation_index'] == row['original_fixation_index'], 'fixation_position_x'].values[0]
                new_y = df_uncorrected.loc[df_uncorrected['fixation_index'] == row['original_fixation_index'], 'fixation_position_y'].values[0]

                df.at[index, 'fixation_position_x'] = new_x
                df.at[index, 'fixation_position_y'] = new_y

        df.to_csv(output_folder / file.name, sep='\t', index=False)


if __name__ == '__main__':
    merge_fixations_and_coordinates()
