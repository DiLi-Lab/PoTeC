from pathlib import Path
from typing import Any

import pandas as pd
import spacy
import spacy_transformers
import benepar


def create_syntax_trees():
    nlp = spacy.load('de_core_news_sm')
    nlp.add_pipe("benepar", config={"model": "benepar_de2"})

    stimuli_file = Path('/Users/debor/repos/PoTeC-data/stimuli/stimuli/stimuli_with_texts.tsv')

    stimuli = pd.read_csv(stimuli_file, sep='\t', keep_default_na=False,
                          na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan',
                                     '1.#IND',
                                     '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a', 'nan', ''])
    const_tree_dfs = []
    dependency_df = pd.DataFrame()

    for idx, text_row in stimuli.iterrows():

        text_id = text_row['text_id']
        text_id_numeric = text_row['text_id_numeric']
        text = text_row['text']

        # create a new df that contains the sentence index, the sentence and the dependency tree
        new_columns = {
            'sent_index_in_text': [],
            'sentence': [],
            'constituency_tree': [],
            'str_constituents': [],
            'pos_tags': [],
            'constituents': [],
        }

        doc = nlp(text)
        sentences = list(doc.sents)
        for sent_index, sent in enumerate(sentences):
            dep_df = _create_dependency_trees(sent)
            dep_df['text_id_numeric'] = text_id_numeric
            dep_df['text_id'] = text_id
            dep_df['sent_index_in_text'] = sent_index + 1
            dependency_df = pd.concat([dependency_df, dep_df])

            tree, constituents, pos = _create_constituency_trees(sent)
            new_columns['sent_index_in_text'].append(sent_index + 1)
            new_columns['sentence'].append(sent)
            new_columns['constituency_tree'].append(tree)
            new_columns['str_constituents'].append([tree])
            new_columns['pos_tags'].append(pos)
            new_columns['constituents'].append(constituents)

        new_df = pd.DataFrame(new_columns)
        new_df['text_id_numeric'] = text_id_numeric
        new_df['text_id'] = text_id
        const_tree_dfs.append(new_df)

    const_tree_df = pd.concat(const_tree_dfs)
    const_tree_df.to_csv('/Users/debor/repos/PoTeC-data/stimuli/constituency_trees.tsv', sep='\t', index=True, index_label='index')

    dependency_df.to_csv('/Users/debor/repos/PoTeC-data/stimuli/dependency_trees.tsv', sep='\t', index=False)


def _create_dependency_trees(sentence: spacy.tokens.span.Span) -> pd.DataFrame:
    word_idx, words, lemmas, pos, tags, deps, heads, heads_pos, children = [], [], [], [], [], [], [], [], []
    for token in sentence:
        word_idx.append(token.i)
        words.append(token.text)
        lemmas.append(token.lemma_)
        pos.append(token.pos_)
        tags.append(token.tag_)
        deps.append(token.dep_)
        heads.append(token.head.text)
        heads_pos.append(token.head.pos_)
        children.append([child for child in token.children])

    df = pd.DataFrame({
        'spacy_word': words,
        'spacy_lemma': lemmas,
        'spacy_pos': pos,
        'spacy_tag': tags,
        'dependency': deps,
        'dependency_head': heads,
        'dependency_head_pos': heads_pos,
        'dependency_children': children
    })

    return df


def _create_constituency_trees(sentence: spacy.tokens.span.Span) -> tuple[Any, list, list]:
    return sentence._.parse_string, list(sentence._.constituents), [token.pos_ for token in sentence]


def main() -> int:

    create_syntax_trees()

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

