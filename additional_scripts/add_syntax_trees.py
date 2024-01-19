from pathlib import Path

import pandas as pd
import spacy
import spacy_transformers
import benepar


def create_syntax_trees():
    nlp = spacy.load('de_core_news_sm')
    nlp.add_pipe("benepar", config={"model": "benepar_de2"})

    stimuli_file = Path('/Users/debor/repos/PoTeC-data/stimuli/stimuli/stimuli.tsv')

    stimuli = pd.read_csv(stimuli_file, sep='\t', keep_default_na=False,
                          na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan',
                                     '1.#IND',
                                     '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan', ''])
    dep_tree_dfs = []

    for idx, text_row in stimuli.iterrows():

        text_id = text_row['text_id']
        text_id_numeric = text_row['text_id_numeric']
        text = text_row['text']

        # create a new df that contains the sentence index, the sentence and the dependency tree
        new_columns = {
            'sent_index_in_text': [],
            'sentence': [],
            'dependency_tree': [],
        }

        doc = nlp(text)
        sentences = list(doc.sents)
        for sent_index, sent in enumerate(sentences):
            _create_dependency_tress(sent)

            tree = sent._.parse_string
            new_columns['sent_index_in_text'].append(sent_index + 1)
            new_columns['sentence'].append(sent)
            new_columns['dependency_tree'].append(tree)

        new_df = pd.DataFrame(new_columns)
        new_df['text_id_numeric'] = text_id_numeric
        new_df['text_id'] = text_id
        dep_tree_dfs.append(new_df)

    dep_tree_df = pd.concat(dep_tree_dfs)
    dep_tree_df.to_csv('stimuli/dependency_trees.tsv', sep='\t', index=False)


def _create_dependency_tress(sentence) -> None:
    for token in sentence:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,)


def _create_constituency_trees() -> None:
    pass


def main() -> int:

    create_syntax_trees()

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

