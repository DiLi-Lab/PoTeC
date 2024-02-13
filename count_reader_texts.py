from collections import Counter
from pathlib import Path
import pandas as pd


def main():
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
            #text_id = file.name.split('_')[1]
            total_texts += 1

            counter.update([reader_id])

        print(folder.name)
        print(len(files))
        print(counter)
        print(len(counter))
        print('\n')
    print(total_texts)


def compute_participant_stats():

    participants_file = Path(__file__).parent / 'participants' / 'participant_data.tsv'
    participants = pd.read_csv(participants_file, sep='\t')
    print(participants.columns)

    mean_vaules = participants[['domain_expert_status', 'reader_domain', 'expert_status', 'age', 'hours_sleep']].groupby(
        ['domain_expert_status', 'reader_domain', 'expert_status']).agg(['mean', 'std'])

    counts = participants[['domain_expert_status', 'reader_domain', 'expert_status', 'glasses', 'handedness', 'alcohol', 'gender']].groupby(
        ['domain_expert_status', 'reader_domain', 'expert_status'])

    l = ['glasses', 'handedness', 'alcohol', 'gender']
    for name, group in counts:
        print(name)
        for i in l:
            print(group[i].value_counts())
        print('\n')
    print(mean_vaules.to_latex())


def main():
    compute_participant_stats()

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
