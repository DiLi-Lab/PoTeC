from collections import Counter
from pathlib import Path


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


if __name__ == '__main__':
    raise SystemExit(main())