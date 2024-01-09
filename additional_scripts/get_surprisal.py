import os
os.environ['CUDA_VISIBLE_DEVICES'] = "1,2,3"
from collections import defaultdict
import pandas as pd
import re
from glob import glob
from pathlib import Path
import pickle
from typing import List
import gc
import torch

STOP_CHARS_SURP = []


class Annotations:
    """
    Class for annotations
    """

    def __init__(
            self,
            stimulus_path
    ):
        self.stimulus_path = stimulus_path
        self.word_features_path = stimulus_path / "word_features"
        self.text_path = stimulus_path / "stimuli"
        self.word_features = self.load_wf_files(self.word_features_path)
        self.stimulus_texts = self.load_stimulus_texts(self.text_path)
        self.word_features_with_punct = self.load_wf_with_punct_files()
        # initialilze defaultdit with empty list
        self.surprisal = defaultdict(list)

    def load_wf_files(self, stimulus_path) -> List[str]:
        # find all files with the pattern word_features_*.tsv
        glob_pattern = os.path.join(stimulus_path, "word_features_*.tsv")
        files = glob(glob_pattern)
        return files
        # return pd.read_csv(stimulus_path, sep="\t")
    
    def load_stimulus_texts(self, stimulus_path) -> pd.DataFrame:
        return pd.read_csv(stimulus_path / "stimuli.tsv", sep="\t")
    
    def load_wf_with_punct_files(self) -> List[str]:
        # first, check if directory exists
        if not os.path.exists(self.stimulus_path / "word_features_with_punct"):
            print('getting punct for word_features files')
            self.get_punct_for_wf_files()
        glob_pattern = os.path.join(self.stimulus_path / "word_features_with_punct", "word_features_*.tsv")
        files = glob(glob_pattern)
        return files

    def get_punct_for_wf_files(self):
            # compute surprisal for each word in each sentence
            # check if surprisal already computed
            if os.path.exists('surprisal.pickle'):
                print('Loading surprisal from pickle file')
                self.surprisal = pickle.load('surprisal.pickle')
            else:
                group_text = self.stimulus_texts.groupby('text_id')
                # test: split at white-spaces and check if words are the same in the word_features file
                for text_id, sub_df in group_text:
                    words = sub_df['text'].astype(str).tolist()[0].split(" ")
                    # find correct word_features file
                    word_features_file = [file for file in self.word_features if text_id in file]
                    assert len(word_features_file) == 1
                    word_features_file = pd.read_csv(word_features_file[0], sep="\t")
                    # add new column in word_features file called "word_with_punct" as second column
                    words_word_features = word_features_file['word'].astype(str).tolist()
                    words_text_files = sub_df['text'].astype(str).tolist()[0].split(" ")
                    word_features_file.insert(1, "word_with_punct", words_text_files)
                    # save word_features_file with new column in directory word_features_with_punct
                    # create new directory if not exists
                    if not os.path.exists(self.stimulus_path / "word_features_with_punct"):
                        os.makedirs(self.stimulus_path / "word_features_with_punct")
                    word_features_file.to_csv(f'{self.stimulus_path / "word_features_with_punct"}/word_features_{text_id}.tsv', sep="\t", index=False)

    def compute_surprisal_from_wf_df(self):
        # compute surprisal for each word in each sentence
        # check if surprisal already computed
        # check if directory for outfiles exists
        if not os.path.exists(self.stimulus_path / "word_features_with_surprisal"):
            os.makedirs(self.stimulus_path / "word_features_with_surprisal")
        if os.path.exists('surprisal.pickle'):
            print('Loading surprisal from pickle file')
            self.surprisal = pickle.load('surprisal.pickle')
        else:
            all_df = pd.concat([pd.read_csv(file, sep="\t") for file in self.word_features_with_punct])
            from surprisal import MultiLMScorer
            multi_scorer = MultiLMScorer()
            for model in multi_scorer.load_models():
                model_name = model.name
                # create new column in all_df for each model (dtype float)
                all_df[f"sent_surprisal_{model_name}"] = 0.0
                all_df[f"text_surprisal_{model_name}"] = 0.0
                all_df['word_with_punct'] = all_df['word_with_punct'].astype(str)
                group_text_sent = all_df.groupby(['text_id', 'sent_index_in_text'])
                group_text = all_df.groupby('text_id')
                # iterate over texts (rows in stimuli.tsv)
                for id_sn, sub_df in group_text_sent:
                    sent = ' '.join(sub_df['word_with_punct'].astype(str).tolist())
                    sent = re.sub(r'\bβ\b', 'beta', sent)
                    sent = re.sub(r'\bπ\b', 'pi', sent)
                    words = sent.split(" ")
                    probs, offset = model.score(sent)
                    surprisal = self.get_per_word_surprisal(offset, probs, sent, words)
                    # add surprisal values to dataframe
                    all_df.loc[(all_df['text_id'] == id_sn[0]) & (all_df['sent_index_in_text'] == id_sn[1]), f"sent_surprisal_{model_name}"] = surprisal
                # split all_df into separate dataframes for each text and save to file
                for text_id, sub_df in group_text:
                    text = ' '.join(sub_df['word_with_punct'].astype(str).tolist())
                    text = re.sub(r'\bβ\b', 'beta', text)
                    text = re.sub(r'\bπ\b', 'pi', text)
                    words = text.split(" ")
                    probs, offset = model.score(text)
                    surprisal = self.get_per_word_surprisal(offset, probs, text, words)
                    # add surprisal values to dataframe
                    all_df.loc[(all_df['text_id'] == text_id), f"text_surprisal_{model_name}"] = surprisal
                del model
                gc.collect()
                torch.cuda.empty_cache()
                    
            for file in self.word_features:
                # read file and get text_id
                temp_df = pd.read_csv(file, sep="\t")
                text_id = temp_df['text_id'].unique()[0]
                # assert that text_id is unique
                assert len(temp_df['text_id'].unique()) == 1
                df = all_df[all_df['text_id'] == text_id]
                # remove old column "surprisal"
                df = df.drop(columns=['surprisal'])
                # save df under same name but with _surprisal.tsv
                df.to_csv(f'{self.stimulus_path / "word_features_with_surprisal"}/word_features_{text_id}.tsv', sep="\t", index=False)

    @staticmethod
    def get_per_word_surprisal(offset, probs, sent, words):
        surprisal = []
        j = 0
        for i in range(0, len(words)):  # i index for reference word list
            try:
                # case 1: tokenized word = white-space separated word
                # print(f'{words[i]} ~ {sent[offset[j][0]:offset[j][1]]}')
                if words[i] == sent[offset[j][0]: offset[j][1]].strip():
                    surprisal += [probs[i]]
                    j += 1
                # case 2: tokenizer split subword tokens: merge subwords and add up surprisal values until the same
                else:
                    concat_token = sent[offset[j][0]: offset[j][1]].strip()
                    concat_surprisal = probs[j]
                    while concat_token != words[i]:
                        j += 1
                        concat_token += sent[
                                        offset[j][0]: offset[j][1]
                                        ].strip()
                        # define characters that should not be added to word surprisal values
                        if (
                                sent[offset[j][0]: offset[j][1]].strip()
                                not in STOP_CHARS_SURP
                        ):
                            concat_surprisal += probs[j]
                        if concat_token == words[i]:
                            surprisal += [concat_surprisal]
                            j += 1
                            break
            except IndexError:
                print(i)
                print(
                    f"Index error in sentence: {sent}, length: {len(sent)} \n problem is after word {words[i]}."
                )
                break
        return surprisal


def main() -> int:
    repo_root = Path(__file__).parent.parent
    word_features = repo_root / "stimuli"

    potec_annotations = Annotations(
        stimulus_path=word_features
    )
    potec_annotations.compute_surprisal_from_wf_df()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
