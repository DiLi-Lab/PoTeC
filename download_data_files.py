import argparse
import os
from pathlib import Path

import requests
from tqdm import tqdm
import zipfile


def download_data(extract: bool) -> None:
    base_url = 'https://osf.io/download/'

    urls = {
        'fixations': '53zwb',
        'fixations_uncorrected': 'd8pyg',
        'raw_data': 'tgd9q',
        'reading_measures': 'g5jds',
        'reading_measures_merged': '3ywhz',
        'scanpaths': 'thgv2',
        'scanpaths_merged': '7fkze',
    }

    folder = Path(__file__).parent / 'eyetracking_data'
    if not os.path.exists(folder):
        os.makedirs(folder)

    for data, resource in (pbar := tqdm(urls.items())):
        pbar.set_description(f'Downloading {"and extracting " if extract else ""}{data}')
        # Downloading the file by sending the request to the URL
        url = base_url + resource

        req = requests.get(url, stream=True)

        # Split URL to get the file name
        filename = f'{data}.zip'
        path = folder / filename
        extract_path = folder / data

        if os.path.exists(path):
            print(f'\nPath for {data} data already exists. Not downloaded to {path}')
            continue

        elif os.path.exists(extract_path):
            print(f'\nPath for {data} data already exists. Not downloaded to {extract_path}')
            continue

        # Writing the file to the local file system
        with open(path, 'wb') as output_file:
            for chunk in req.iter_content(chunk_size=128):
                output_file.write(chunk)

        if extract:
            extract_path = folder
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            os.remove(path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download and extract eyetracking data from the PoTeC OSF repository.'
    )
    parser.add_argument(
        '--extract',
        action='store_true',
        help='Extract downloaded data.',
        default=True,
    )

    args = parser.parse_args()
    download_data(args.extract)


