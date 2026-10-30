"""Test reading measures and accuracy."""

import json
import tempfile
import unittest
from itertools import groupby, product
from pathlib import Path

import pandas as pd

from additional_scripts.compute_reading_measures import compute_reading_measures


class ComputeReadingMeasuresTest(unittest.TestCase):
    def compute(self, fixations, text_accuracy=(1, 1, 1), background_accuracy=(1, 1, 1)):
        """Export measures for a three-word text."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('fixations', 'aoi', 'words'):
                (root / name).mkdir()
            pd.DataFrame([{
                'reader_id': 0, 'reader_discipline_numeric': 0, 'gender_numeric': 0,
                'level_of_studies_numeric': 1, 'discipline_level_of_studies_numeric': 0,
                'age': 25,
            }]).to_csv(root / 'participants.tsv', sep='\t', index=False)
            pd.DataFrame([{'text_id': 'b0', 'text_id_numeric': 0}]).to_csv(
                root / 'stimuli.tsv', sep='\t', index=False,
            )
            (root / 'word_limits.json').write_text(json.dumps({'b0': [[1, 5, 9], [3, 7, 11]]}))
            (root / 'sent_limits.json').write_text(json.dumps({'b0': [[1], [3]]}))
            pd.DataFrame({'aoi': [3, 7, 11], 'line': [1, 1, 1]}).to_csv(
                root / 'aoi/b0.ias', sep='\t', index=False,
            )
            pd.DataFrame({
                'word_index_in_sent': [1, 2, 3], 'sent_index_in_text': [1, 1, 1],
                'word_limit_char_indices': ['1,3', '5,7', '9,11'],
            }).to_csv(root / 'words/word_features_b0.tsv', sep='\t', index=False)
            rows = []
            for index, (aoi, duration) in enumerate(fixations, start=1):
                rows.append({
                    'fixation_index': index, 'aoi': aoi, 'fixation_duration': duration,
                    'text_domain': 'biology', 'text_id': 'b0', 'trial': 7,
                    **{f'acc_{kind}_{question}': value
                       for kind, values in (('tq', text_accuracy), ('bq', background_accuracy))
                       for question, value in enumerate(values, start=1)},
                })
            pd.DataFrame(rows).to_csv(root / 'fixations/reader0_b0_fixations.tsv', sep='\t', index=False)
            compute_reading_measures(
                root / 'fixations', root / 'output', root / 'participants.tsv',
                root / 'word_limits.json', root / 'sent_limits.json', root / 'aoi',
                root / 'words', root / 'stimuli.tsv',
            )
            return pd.read_csv(root / 'output/reader0_b0_rm.tsv', sep='\t').set_index('word_index_in_sent')

    def test_single_fixation(self):
        result = self.compute([(5, 200)])
        for measure in ('FD', 'FFD', 'SFD', 'FRT', 'FPRT', 'TFT', 'RBRT', 'RPD_inc'):
            self.assertEqual(result.loc[2, measure], 200, measure)
        self.assertEqual(result.loc[2, 'TFC'], 1)
        self.assertEqual(result.loc[2, 'TRC_out'], 0)
        self.assertEqual(result.loc[2, 'SL_out'], 0)
        self.assertEqual(result.loc[2, 'trial'], 7)
        self.assertEqual(result.TFT.sum(), 200)

    def test_final_fixation_on_a_new_word(self):
        result = self.compute([(1, 100), (5, 200)])
        self.assertEqual(result.loc[1, 'TFT'], 100)
        self.assertEqual(result.loc[2, 'FD'], 200)
        self.assertEqual(result.loc[2, 'FRT'], 200)
        self.assertEqual(result.loc[2, 'TFT'], 200)
        self.assertEqual(result.TFC.sum(), 2)

    def test_final_fixation_closes_first_run(self):
        result = self.compute([(1, 100), (2, 150)])
        self.assertEqual(result.loc[1, 'FD'], 100)
        for measure in ('FRT', 'FPRT', 'TFT', 'RBRT', 'RPD_inc'):
            self.assertEqual(result.loc[1, measure], 250, measure)
        self.assertEqual(result.loc[1, 'TFC'], 2)
        self.assertEqual(result.loc[1, 'TRC_out'], 0)

    def test_final_fixation_is_a_regression(self):
        result = self.compute([(1, 100), (5, 200), (1, 300)])
        self.assertEqual(result.loc[1, 'TFT'], 400)
        self.assertEqual(result.loc[1, 'FRT'], 100)
        self.assertEqual(result.loc[1, 'FPRT'], 100)
        self.assertEqual(result.loc[1, 'RRT'], 300)
        self.assertEqual(result.loc[2, 'RPD_exc'], 300)
        self.assertEqual(result.loc[2, 'RPD_inc'], 500)
        self.assertEqual(result.TFC.sum(), 3)

    def test_off_word_events_after_final_fixation(self):
        result = self.compute([(1, 100), (5, 200), (4, 50), (0, 60), ('NA', 70)])
        self.assertEqual(result.loc[2, 'FRT'], 200)
        self.assertEqual(result.TFT.sum(), 300)
        self.assertEqual(result.TFC.sum(), 2)

    def test_no_word_fixations(self):
        result = self.compute([(0, 100), (4, 200)])
        self.assertEqual(result.TFT.sum(), 0)
        self.assertEqual(result.TFC.sum(), 0)

    def test_zero_duration_is_not_end_of_stream(self):
        result = self.compute([(1, 100), (2, 0), (3, 150)])
        self.assertEqual(result.loc[1, 'FRT'], 250)
        self.assertEqual(result.loc[1, 'TFT'], 250)
        self.assertEqual(result.loc[1, 'TFC'], 3)

    def test_accuracy_uses_only_source_rows(self):
        result = self.compute([(1, 100), (5, 200)])
        for column in ('acc_bq_1', 'acc_bq_2', 'acc_bq_3', 'acc_tq_1', 'acc_tq_2', 'acc_tq_3',
                       'mean_acc_bq', 'mean_acc_tq'):
            self.assertTrue(result[column].eq(1).all(), column)

    def test_terminal_zero_duration(self):
        result = self.compute([(1, 100), (5, 0)])
        self.assertEqual(result.loc[2, 'TFC'], 1)
        self.assertEqual(result.loc[2, 'TFT'], 0)
        self.assertEqual(result.TFC.sum(), 2)

    def test_accuracy_matches_question_type(self):
        for text_accuracy, background_accuracy in (
                ((1, 1, 0), (0, 0, 1)), ((0, 0, 1), (1, 1, 0))):
            with self.subTest(text=text_accuracy, background=background_accuracy):
                result = self.compute([(1, 100), (5, 200)], text_accuracy, background_accuracy)
                for kind, values in (('tq', text_accuracy), ('bq', background_accuracy)):
                    for question, value in enumerate(values, start=1):
                        self.assertTrue(result[f'acc_{kind}_{question}'].eq(value).all())
                    for actual in result[f'mean_acc_{kind}']:
                        self.assertAlmostEqual(actual, sum(values) / 3)

    def test_short_sequences(self):
        for length in range(1, 5):
            for words in product((0, 1, 2), repeat=length):
                with self.subTest(words=words):
                    events = [(word, 10 * (i + 1)) for i, word in enumerate(words)]
                    result = self.compute([({0: 0, 1: 1, 2: 5}[w], d) for w, d in events])
                    on_text = [(w, d) for w, d in events if w]
                    runs = [(w, sum(d for _, d in group))
                            for w, group in groupby(on_text, key=lambda event: event[0])]
                    for word in (1, 2, 3):
                        durations = [d for w, d in on_text if w == word]
                        self.assertEqual(result.loc[word, 'TFC'], len(durations))
                        self.assertEqual(result.loc[word, 'TFT'], sum(durations))
                        self.assertEqual(result.loc[word, 'FD'], durations[0] if durations else 0)
                        self.assertEqual(result.loc[word, 'FRT'], next(
                            (duration for w, duration in runs if w == word), 0))


if __name__ == '__main__':
    unittest.main()
