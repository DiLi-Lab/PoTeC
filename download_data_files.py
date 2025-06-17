import argparse
import os
from pathlib import Path

import requests
from tqdm import tqdm
import zipfile


def download_data(extract: bool, output_folder: str, download_asc: bool, download_fixations: bool,
                  download_fixations_uncorrected, download_raw_data, download_reading_measures,
                  download_reading_measures_merged, download_scanpaths, download_scanpaths_merged) -> None:
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
        if data == 'fixations' and not download_fixations:
            continue
        if data == 'fixations_uncorrected' and not download_fixations_uncorrected:
            continue
        if data == 'raw_data' and not download_raw_data:
            continue
        if data == 'reading_measures' and not download_reading_measures:
            continue
        if data == 'reading_measures_merged' and not download_reading_measures_merged:
            continue
        if data == 'scanpaths' and not download_scanpaths:
            continue
        if data == 'scanpaths_merged' and not download_scanpaths_merged:
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
        '--fixations',
        dest='download_fixations',
        action='store_true',
        help='Whether to download the fixations files. Default is True.',
        default=True,
    )

    parser.add_argument(
        '--fixations_uncorrected',
        dest='download_fixations_uncorrected',
        action='store_true',
        help='Whether to download the fixations_uncorrected files. Default is False.',
        default=False,
    )

    parser.add_argument(
        '--raw_data',
        dest='download_raw_data',
        action='store_true',
        help='Whether to download the raw_data files. Default is True.',
        default=True,
    )

    parser.add_argument(
        '--reading_measures',
        dest='download_reading_measures',
        action='store_true',
        help='Whether to download the reading_measures files. Default is False.',
        default=False,
    )

    parser.add_argument(
        '--reading_measures_merged',
        dest='download_reading_measures_merged',
        action='store_true',
        help='Whether to download the reading_measures_merged files. Default is True.',
        default=True,
    )

    parser.add_argument(
        '--scanpaths',
        dest='download_scanpaths',
        action='store_true',
        help='Whether to download the scanpaths files. Default is False.',
        default=False,
    )

    parser.add_argument(
        '--scanpaths_merged',
        dest='download_scanpaths_merged',
        action='store_true',
        help='Whether to download the scanpaths_merged files. Default is True.',
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
    download_data(args.extract, args.output_folder, args.download_asc, args.download_fixations,
                  args.download_fixations_uncorrected, args.download_raw_data, args.download_reading_measures,
                  args.download_reading_measures_merged, args.download_scanpaths, args.download_scanpaths_merged)


