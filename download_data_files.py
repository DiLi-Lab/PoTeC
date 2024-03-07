import argparse
import os
from pathlib import Path

import requests
from tqdm import tqdm
import zipfile


def download_data(extract: bool, download_asc: bool, output_folder: str) -> None:
    base_url = 'https://osf.io/download/'

    urls = {
        'fixations': '53zwb',
        'fixations_uncorrected': 'd8pyg',
        'raw_data': 'tgd9q',
        'reading_measures': 'g5jds',
        'reading_measures_merged': '3ywhz',
        'scanpaths': 'thgv2',
        'scanpaths_merged': '7fkze',
        'asc_files': 'zgx2u',
    }

    folder = Path(__file__).parent / output_folder
    if not os.path.exists(folder):
        os.makedirs(folder)

    for data, resource in (pbar := tqdm(urls.items())):
        if data == 'asc_files' and not download_asc:
            continue

        pbar.set_description(f'Downloading {"and extracting " if extract else ""}{data}')
        # Downloading the file by sending the request to the URL
        url = base_url + resource

        req = requests.get(url, stream=True)

        # create new paths for the downloaded files
        filename = f'{data}.zip'
        path = folder / filename
        extract_path = folder / data

        if os.path.exists(path):
            print(f'\nPath for {data} already exists. Not downloaded to {path}')
            continue

        elif os.path.exists(extract_path):
            print(f'\nPath for {data} already exists. Not downloaded to {extract_path}')
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

    parser.add_argument(
        '--asc',
        dest='download_asc',
        action='store_true',
        help='Whether to download the asc files. Default is False.',
        default=False,
    )

    parser.add_argument(
        '-o', '--output-folder',
        dest='output_folder',
        type=str,
        help='Path to the output folder. Default is eyetracking_data',
        default='eyetracking_data'
    )

    args = parser.parse_args()
    download_data(args.extract, args.download_asc, args.output_folder)


