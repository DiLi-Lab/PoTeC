from collections import defaultdict
import pandas as pd
import re
from glob import glob
from pathlib import Path
import os
import pickle
import spacy

# Path("./pl_analysis/reading_measures").mkdir(exist_ok=True)
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
        self.stimuli = self.load_stimuli(stimulus_path)
        # initialilze defaultdit with empty list
        self.surprisal = defaultdict(list)

    def load_stimuli(self, stimulus_path) -> pd.DataFrame:
        # find all files with the pattern word_features_*.tsv
        glob_pattern = os.path.join(stimulus_path, "word_features_*.tsv")
        files = glob(glob_pattern)
        return files
        # return pd.read_csv(stimulus_path, sep="\t")

    def compute_surprisal(self):
        from Surprisal import SurprisalScorer
        S = SurprisalScorer(model_name="gpt")
        # compute surprisal for each word in each sentence
        # check if surprisal already computed
        if os.path.exists('surprisal.pickle'):
            self.surprisal = pickle.load('surprisal.pickle')
        else:
            # iterate over texts (rows in stimuli.tsv)
            for file in self.stimuli:
                all_surprisal = []
                df = pd.read_csv(file, sep="\t")
                df['word'] = df['word'].astype(str)
                grouped_df = df.groupby('sent_index_in_text')
                # join words in each sentence, force to string
                sents = grouped_df['word'].agg(' '.join)
                for sent in sents:
                    # replace all greek symbols with their names
                    sent = re.sub(r'\bβ\b', 'beta', sent)
                    sent = re.sub(r'\bπ\b', 'pi', sent)
                    words = sent.split(" ")
                    probs, offset = S.score(sent)
                    surprisal = self.get_per_word_surprisal(offset, probs, sent, words)
                    all_surprisal.extend(surprisal)
                df['surprisal'] = all_surprisal
                out_file = f'{self.stimulus_path}/{file.split("/")[-1]}'
                df.to_csv(out_file, sep="\t", index=False)
    

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
                print(
                    f"Index error in sentence: {sent}, length: {len(sent)} \n problem is after word {words[i]}."
                )
                break
        return surprisal

def main() -> int:
    potec_annotations = Annotations(
        stimulus_path=Path("./stimuli/word_features/")
    )
    potec_annotations.compute_surprisal()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

