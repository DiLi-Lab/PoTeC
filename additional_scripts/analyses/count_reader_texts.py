from collections import Counter
from pathlib import Path
import pandas as pd


def count_reader_files() -> None:
    """
    Count the number of files for each reader in the eyetracking_data folders
    """
    # this files path
    path = Path(__file__).parent
    et_folders = [
        path / 'eyetracking_data' / 'reading_measures',
        path / 'eyetracking_data' / 'reading_measures_merged',
        path / 'eyetracking_data' / 'fixations',
        path / 'eyetracking_data' / 'fixations_uncorrected',
        path / 'eyetracking_data' / 'raw_data',
        path / 'eyetracking_data' / 'scanpaths',
        path / 'eyetracking_data' / 'scanpaths_merged',
    ]

    total_texts = 0
    for folder in et_folders:
        counter = Counter()
        files = list(folder.glob('*.tsv'))
        for file in files:
            reader_id = file.name.split('_')[0]
            # text_id = file.name.split('_')[1]
            total_texts += 1

            counter.update([reader_id])

        print(folder.name)
        print(len(files))
        print(counter)
        print(len(counter))
        print('\n')
    print(total_texts)


def compute_participant_stats() -> None:
    """
    Create and print a latex table with an overview over participant features
    """

    participants_file = Path(__file__).parent / 'participants' / 'participant_data.tsv'
    participants = pd.read_csv(participants_file, sep='\t')
    print(participants.columns)

    mean_vaules = participants[
        ['discipline_level_of_studies', 'reader_discipline', 'level_of_studies', 'age',
         'hours_sleep']
    ].groupby(
        ['discipline_level_of_studies', 'reader_discipline', 'level_of_studies']
    ).agg(['mean', 'std'])

    counts = participants[
        ['discipline_level_of_studies', 'reader_discipline', 'level_of_studies', 'glasses',
         'handedness', 'alcohol', 'gender']
    ].groupby(
        ['discipline_level_of_studies', 'reader_discipline', 'level_of_studies']
    )

    l = ['glasses', 'handedness', 'alcohol', 'gender']
    for name, group in counts:
        print(name)
        for i in l:
            print(group[i].value_counts())
        print('\n')
    print(mean_vaules.to_latex())


def main():
    # count_reader_files()
    compute_participant_stats()

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
