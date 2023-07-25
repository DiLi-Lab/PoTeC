#!/usr/bin/env python3
"""
TODO: clean again, r is never closed?
Call: python3 merge_reading_measures+word_features.py
To specify custom file paths see argparse arguments at the bottom of the file.
"""
import argparse
import csv
import os
from pathlib import Path

import pandas as pd
from tqdm import tqdm


def merge_rm_word_features(
        reading_measure_folder: str,
        word_features_folder: str,
        text_tags_folder: str,
        reader_ids_file: str,
        output_folder: str,
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    r = open(reader_ids_file, 'r')  # open file containing all reader ids as a list in one line
    reader = csv.reader(r, delimiter='\t')
    reader_ids = [int(r) for r in sorted(next(reader))]
    # remove readers with bad calibration:
    # bad_cali = []
    # # bad_cali = [2, 9, 16, 19, 22, 31, 39, 41, 64, 72, 83, 85, 90, 93]
    # [reader_ids.remove(r) for r in bad_cali]
    texts = ['b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'p0', 'p1', 'p2', 'p3', 'p4', 'p5']

    # Read and merge data

    # Read text features
    for textIndex, text in tqdm(enumerate(texts), desc='Merging files...', total=len(texts)):
        filename_tags = os.path.join(text_tags_folder, text + '.tags')
        filename_features = os.path.join(word_features_folder, 'word_features_' + text + '.txt')

        word_tags = pd.read_csv(
            filename_tags, sep='\t', na_values=['None', '.', 'NA'],
            usecols=['WORD', 'TechnialTerm', 'WordIndexInSentence', 'SentenceIndex', 'WordLen',
                     'WordIndexInText', 'Quote', 'Parentheses', 'ClauseBegin', 'SentenceBegin',
                     'isAbbr', 'containsAbbr', 'Hyph', 'Symbol', 'PRELS', 'PRELAT', 'PPOSAT',
                     'PPER',
                     'PPOSS', 'PIDAT', 'PIAT', 'PIS', 'PDAT', 'PDS', 'NN', 'NE', 'KOKOM', 'KON',
                     'KOUS', 'KOUI', 'ITJ', 'FM', 'CARD', 'ART', 'APZR', 'APPO', 'APPRART', 'APPR',
                     'ADV', 'ADJD', 'ADJA', 'XY', 'VMPP', 'VMINF', 'VMFIN', 'VAPP', 'VAFIN', 'VVPP',
                     'VVIZU', 'VVINF', 'VVIMP', 'VVFIN', 'TRUNC', 'PTKA', 'PTKANT', 'PTKVZ',
                     'PTKNEG', 'PTKZU', 'PAV', 'PWAV', 'PWAT', 'PWS', 'PRF'],
            encoding='utf-8',
        )
        word_features = pd.read_csv(
            filename_features, sep='\s+', na_values=['None', '.', 'NA'],
            usecols=['Type', 'Lemma', 'Lemma_length_(characters)', 'Type_length_(syllables)',
                     'Annotated_type_frequency_normalized', 'Type_frequency_normalized',
                     'Lemma_frequency_normalized', 'Familiarity_normalized',
                     'Regularity_normalized', 'Document_frequency_normalized',
                     'Sentence_frequency_normalized',
                     'Cumulative_syllable_corpus_frequency_normalized',
                     'Cumulative_syllable_lexicon_frequency_normalized',
                     'Cumulative_character_corpus_frequency_normalized',
                     'Cumulative_character_lexicon_frequency_normalized',
                     'Cumulative_character_bigram_corpus_frequency_normalized',
                     'Cumulative_character_bigram_lexicon_frequency_normalized',
                     'Cumulative_character_trigram_corpus_frequency_normalized',
                     'Cumulative_character_trigram_lexicon_frequency_normalized',
                     'Initial_letter_frequency_normalized',
                     'Initial_bigram_frequency_normalized',
                     'Initial_trigram_frequency_normalized', 'Avg._cond._prob.,_in_bigrams',
                     'Avg._cond._prob.,_in_trigrams',
                     'Neighbors_Coltheart_higher_freq.,_cum._freq.,_normalized',
                     'Neighbors_Coltheart_higher_freq.,_count,_normalized',
                     'Neighbors_Coltheart_all,_cum._freq.,_normalized',
                     'Neighbors_Coltheart_all,_count,_normalized',
                     'Neighbors_Levenshtein_higher_freq.,_cum._freq.,_normalized',
                     'Neighbors_Levenshtein_higher_freq.,_count,_normalized',
                     'Neighbors_Levenshtein_all,_cum._freq.,_normalized',
                     'Neighbors_Levenshtein_all,_count,_normalized'],
            encoding='utf-8',
            engine='python',
        )

        # concatenate word_features and word_tags (i.e., just add columns; their order is identical)
        text_features = pd.concat([word_tags, word_features], axis=1)
        text_features = text_features.reindex(word_tags.index)

        # replace missing values with 0s (affects frequency measures: if word does not occur in corpus, frequency = 0)
        text_features = text_features.fillna(0)

        # add Eye movements data for each reader
        for readerIndex, reader in enumerate(reader_ids):
            filename_reading_measures = os.path.join(
                reading_measure_folder,
                'reader' + str(reader) + '_' + text + '_rm.csv'
            )
            reading_measure_csv = pd.read_csv(
                filename_reading_measures,
                sep='\t',
                na_values=['None', '.', 'NA'],
                usecols=['FRT', 'SL_out', 'TRC_in', 'FFD', 'FPRT', 'RPD_exc', 'TFT', 'RRT', 'FPF', 'FD', 'RR', 'Fix',
                         'LP', 'WordIndexSent', 'SL_in', 'RPD_inc', 'FPReg', 'TRC_out', 'SentIndex', 'SFD', 'RBRT',
                         'topic', 'trial', 'gender', 'major', 'expert_status', 'age', 'ACC_B_Q1', 'ACC_B_Q2',
                         'ACC_B_Q3',
                         'ACC_T_Q1', 'ACC_T_Q2', 'ACC_T_Q3', 'meanAccBQ', 'meanAccTQ', 'group', 'itemid', 'reader']
            )

            # sort columns. Necessary because different col ordering in different input files
            reading_measure_csv = reading_measure_csv[
                ["WordIndexSent", "SentIndex", "FFD", "SFD", "FD", "FPRT", "FRT", "TFT", "RRT", "RPD_inc", "RPD_exc",
                 "RBRT", "Fix", "FPF", "RR", "FPReg", "TRC_out", "TRC_in", "LP", "SL_in", "SL_out", "ACC_B_Q1",
                 "ACC_B_Q2", "ACC_B_Q3", "ACC_T_Q1", "ACC_T_Q2", "ACC_T_Q3", "meanAccTQ", "meanAccBQ", "topic", "trial",
                 "itemid", "reader", "gender", "major", "expert_status", "age", "group"]
            ]

            # concatenate text features with eye movements
            data = pd.concat([text_features, reading_measure_csv], axis=1)

            # write merged data
            filename_merged_data = os.path.join(output_folder, 'reader' + str(reader) + '_' + text + '_merged.txt')
            data.to_csv(path_or_buf=filename_merged_data, header=True, na_rep='NA', sep='\t', index=False)


def create_parser():
    base_path = Path(os.getcwd()).parent
    pars = argparse.ArgumentParser()

    pars.add_argument(
        '--reading_measure_folder',
        default=base_path / 'eyetracking_data/reading_measures',
    )

    pars.add_argument(
        '--word_features_folder',
        default=base_path / 'stimuli/word_features',
    )

    pars.add_argument(
        '--text_tags_folder',
        default=base_path / 'stimuli/text_tags',
    )

    pars.add_argument(
        '--reader_ids_file',
        default=base_path / 'participants/readerIDs.txt',
    )

    pars.add_argument(
        '--output_folder',
        default=base_path / 'eyetracking_data/rm_word_features',
    )

    return pars


if __name__ == '__main__':
    parser = create_parser()
    args = vars(parser.parse_args())
    merge_rm_word_features(**args)
