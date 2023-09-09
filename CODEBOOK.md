# Codebook

## Stimuli

[Text and comprehension questions](stimuli/texts_and_questions)




[Word features](stimuli/OLD/word_features)




todos:
- check whether text and word columns are always exactly equal, if yes, delete text, but move word to the first column
  - there are some that are not the same, why??

| Column                                                    | Data type   | Description   |
|:----------------------------------------------------------|:------------|:--------------|
| text                                                      | object      | <NA>          |
| STTS-tag                                                  | object      | <NA>          |
| line_index                                                | int64       | <NA>          |
| word                                                      | object      | <NA>          |
| type                                                      | object      | <NA>          |
| type_length_chars                                         | float64     | <NA>          |
| PoS_tag                                                   | object      | <NA>          |
| lemma                                                     | object      | <NA>          |
| lemma_length_chars                                        | float64     | <NA>          |
| syllables                                                 | object      | <NA>          |
| type_length_syllables                                     | float64     | <NA>          |
| annotated_type_frequency_normalized                       | float64     | <NA>          |
| type_frequency_normalized                                 | float64     | <NA>          |
| lemma_frequency_normalized                                | float64     | <NA>          |
| familiarity_normalized                                    | float64     | <NA>          |
| regularity_normalized                                     | float64     | <NA>          |
| document_frequency_normalized                             | float64     | <NA>          |
| sentence_frequency_normalized                             | float64     | <NA>          |
| cumulative_syllable_corpus_frequency_normalized           | float64     | <NA>          |
| cumulative_syllable_lexicon_frequency_normalized          | float64     | <NA>          |
| cumulative_character_corpus_frequency_normalized          | float64     | <NA>          |
| cumulative_character_lexicon_frequency_normalized         | float64     | <NA>          |
| cumulative_character_bigram_corpus_frequency_normalized   | float64     | <NA>          |
| cumulative_character_bigram_lexicon_frequency_normalized  | float64     | <NA>          |
| cumulative_character_trigram_corpus_frequency_normalized  | float64     | <NA>          |
| cumulative_character_trigram_lexicon_frequency_normalized | float64     | <NA>          |
| initial_letter_frequency_normalized                       | float64     | <NA>          |
| initial_bigram_frequency_normalized                       | float64     | <NA>          |
| initial_trigram_frequency_normalized                      | float64     | <NA>          |
| avg_cond_prob_in_bigrams                                  | float64     | <NA>          |
| avg_cond_prob_in_trigrams                                 | float64     | <NA>          |
| neighbors_coltheart_higher_freq_cum_freq_normalized       | float64     | <NA>          |
| neighbors_coltheart_higher_freq_count_normalized          | float64     | <NA>          |
| neighbors_coltheart_all_cum_freq_normalized               | float64     | <NA>          |
| neighbors_coltheart_all_count_normalized                  | float64     | <NA>          |
| neighbors_levenshtein_higher_freq_cum_freq_normalized     | float64     | <NA>          |
| neighbors_levenshtein_higher_freq_count_normalized        | float64     | <NA>          |
| neighbors_levenshtein_all_cum_freq_normalized             | float64     | <NA>          |
| neighbors_levenshtein_all_count_normalized                | float64     | <NA>          |

[Text tags](stimuli/OLD/text_tags)

| Column                  | Data type | Description                                                                                                                                              |
|:------------------------|:----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| word_index_in_text      | int64     | <NA>                                                                                                                                                     |
| word                    | object    | <NA>                                                                                                                                                     |
| STTS_PoS_tag            | object    | <NA>                                                                                                                                                     |
| is_technical_term       | int64     | <NA>                                                                                                                                                     |
| is_abbreviation         | int64     | <NA>                                                                                                                                                     |
| word_index_in_sent      | int64     | <NA>                                                                                                                                                     |
| sent_index_in_text      | int64     | <NA>                                                                                                                                                     |
| word_length             | int64     | word length in number of characters without sentence punctuation at the end (i.e., z.B. = 4 characters; DNA-Kette =9 characters; [He] eats.=4 characters |
| STTS_punctuation_before | object    | <NA>                                                                                                                                                     |
| STTS_punctuation_after  | object    | <NA>                                                                                                                                                     |
| word_limit_char_indices | object    | <NA>                                                                                                                                                     |
| text_id                 | object    | <NA>                                                                                                                                                     |
| is_in_quote             | int64     | <NA>                                                                                                                                                     |
| is_in_parentheses       | int64     | <NA>                                                                                                                                                     |
| contains_symbol         | int64     | <NA>                                                                                                                                                     |
| contains_hyphen         | int64     | <NA>                                                                                                                                                     |
| is_clause_beginning     | int64     | <NA>                                                                                                                                                     |
| is_sent_beginning       | int64     | <NA>                                                                                                                                                     |
| contains_abbreviation   | int64     | <NA>                                                                                                                                                     |
| PRELS                   | int64     | <NA>                                                                                                                                                     |
| PRELAT                  | int64     | <NA>                                                                                                                                                     |
| PPOSAT                  | int64     | <NA>                                                                                                                                                     |
| PPER                    | int64     | <NA>                                                                                                                                                     |
| PPOSS                   | int64     | <NA>                                                                                                                                                     |
| PIDAT                   | int64     | <NA>                                                                                                                                                     |
| PIAT                    | int64     | <NA>                                                                                                                                                     |
| PIS                     | int64     | <NA>                                                                                                                                                     |
| PDAT                    | int64     | <NA>                                                                                                                                                     |
| PDS                     | int64     | <NA>                                                                                                                                                     |
| NN                      | int64     | <NA>                                                                                                                                                     |
| NE                      | int64     | <NA>                                                                                                                                                     |
| KOKOM                   | int64     | <NA>                                                                                                                                                     |
| KON                     | int64     | <NA>                                                                                                                                                     |
| KOUS                    | int64     | <NA>                                                                                                                                                     |
| KOUI                    | int64     | <NA>                                                                                                                                                     |
| ITJ                     | int64     | <NA>                                                                                                                                                     |
| FM                      | int64     | <NA>                                                                                                                                                     |
| CARD                    | int64     | <NA>                                                                                                                                                     |
| ART                     | int64     | <NA>                                                                                                                                                     |
| APZR                    | int64     | <NA>                                                                                                                                                     |
| APPO                    | int64     | <NA>                                                                                                                                                     |
| APPRART                 | int64     | <NA>                                                                                                                                                     |
| APPR                    | int64     | <NA>                                                                                                                                                     |
| ADV                     | int64     | <NA>                                                                                                                                                     |
| ADJD                    | int64     | <NA>                                                                                                                                                     |
| ADJA                    | int64     | <NA>                                                                                                                                                     |
| XY                      | int64     | <NA>                                                                                                                                                     |
| VMPP                    | int64     | <NA>                                                                                                                                                     |
| VMINF                   | int64     | <NA>                                                                                                                                                     |
| VMFIN                   | int64     | <NA>                                                                                                                                                     |
| VAPP                    | int64     | <NA>                                                                                                                                                     |
| VAFIN                   | int64     | <NA>                                                                                                                                                     |
| VVPP                    | int64     | <NA>                                                                                                                                                     |
| VVIZU                   | int64     | <NA>                                                                                                                                                     |
| VVINF                   | int64     | <NA>                                                                                                                                                     |
| VVIMP                   | int64     | <NA>                                                                                                                                                     |
| VVFIN                   | int64     | <NA>                                                                                                                                                     |
| TRUNC                   | int64     | <NA>                                                                                                                                                     |
| PTKA                    | int64     | <NA>                                                                                                                                                     |
| PTKANT                  | int64     | <NA>                                                                                                                                                     |
| PTKVZ                   | int64     | <NA>                                                                                                                                                     |
| PTKNEG                  | int64     | <NA>                                                                                                                                                     |
| PTKZU                   | int64     | <NA>                                                                                                                                                     |
| PAV                     | int64     | <NA>                                                                                                                                                     |
| PWAV                    | int64     | <NA>                                                                                                                                                     |
| PWAT                    | int64     | <NA>                                                                                                                                                     |
| PWS                     | int64     | <NA>                                                                                                                                                     |
| PRF                     | int64     | <NA>                                                                                                                                                     |

[Aoi](./stimuli/aoi_texts/aoi)

| Column    | Data type   | Description   |
|:----------|:------------|:--------------|
| ?         | int64       | <NA>          |
| ?         | object      | <NA>          |
| roi       | int64       | <NA>          |
| ?         | int64       | <NA>          |
| ?         | int64       | <NA>          |
| ?         | int64       | <NA>          |
| ?         | int64       | <NA>          |
| Character | object      | <NA>          |

## Eye-tracking data

[Fixations](./eyetracking_data/fixations)

TODO:
- (uncorrected) fixation data: is the value of the RECORDING_SESSION_LABEL column always identical to the reader-ID in the filename?

| Column                    | Data type   | Description   |
|:--------------------------|:------------|:--------------|
| fixation_index            | int64       | <NA>          |
| topic                     | object      | <NA>          |
| trial                     | int64       | <NA>          |
| acc_bq_1                  | int64       | <NA>          |
| acc_bq_2                  | int64       | <NA>          |
| acc_bq_3                  | int64       | <NA>          |
| acc_tq_1                  | int64       | <NA>          |
| acc_tq_2                  | int64       | <NA>          |
| acc_tq_3                  | int64       | <NA>          |
| fixation_duration         | int64       | <NA>          |
| next_saccade_duration     | int64       | <NA>          |
| previous_saccade_duration | int64       | <NA>          |
| version                   | int64       | <NA>          |
| line                      | int64       | <NA>          |
| roi                       | int64       | <NA>          |
| index_in_line             | int64       | <NA>          |
| original_fixation_index   | int64       | <NA>          |
| is_fixation_adjusted      | bool        | <NA>          |
| reader_id                 | int64       | <NA>          |
| text_id                   | object      | <NA>          |


[Reading measures](./eyetracking_data/reading_measures)

| Column               | Data type   | Description   |
|:---------------------|:------------|:--------------|
| word_index_in_sent   | int64       | <NA>          |
| sent_index_in_text   | int64       | <NA>          |
| FFD                  | int64       | <NA>          |
| SFD                  | int64       | <NA>          |
| FD                   | int64       | <NA>          |
| FPRT                 | int64       | <NA>          |
| FRT                  | int64       | <NA>          |
| TFT                  | int64       | <NA>          |
| RRT                  | int64       | <NA>          |
| RPD_inc              | int64       | <NA>          |
| RPD_exc              | int64       | <NA>          |
| RBRT                 | int64       | <NA>          |
| Fix                  | int64       | <NA>          |
| FPF                  | int64       | <NA>          |
| RR                   | int64       | <NA>          |
| FPReg                | int64       | <NA>          |
| TRC_out              | int64       | <NA>          |
| TRC_in               | int64       | <NA>          |
| LP                   | int64       | <NA>          |
| SL_in                | int64       | <NA>          |
| SL_out               | int64       | <NA>          |
| acc_bq_1             | float64     | <NA>          |
| acc_bq_2             | float64     | <NA>          |
| acc_bq_3             | float64     | <NA>          |
| acc_tq_1             | float64     | <NA>          |
| acc_tq_2             | float64     | <NA>          |
| acc_tq_3             | float64     | <NA>          |
| topic                | int64       | <NA>          |
| trial                | int64       | <NA>          |
| text_id              | object      | <NA>          |
| reader               | int64       | <NA>          |
| gender               | int64       | <NA>          |
| major                | int64       | <NA>          |
| expert_status        | int64       | <NA>          |
| age                  | float64     | <NA>          |
| mean_acc_bq          | float64     | <NA>          |
| mean_acc_tq          | float64     | <NA>          |
| domain_expert_status | int64       | <NA>          |

[Scanpaths](./eyetracking_data/scanpaths)

| Column                    | Data type   | Description   |
|:--------------------------|:------------|:--------------|
| fixation_index            | int64       | <NA>          |
| topic                     | object      | <NA>          |
| trial                     | int64       | <NA>          |
| acc_bq_1                  | int64       | <NA>          |
| acc_bq_2                  | int64       | <NA>          |
| acc_bq_3                  | int64       | <NA>          |
| acc_tq_1                  | int64       | <NA>          |
| acc_tq_2                  | int64       | <NA>          |
| acc_tq_3                  | int64       | <NA>          |
| fixation_duration         | int64       | <NA>          |
| next_saccade_duration     | int64       | <NA>          |
| previous_saccade_duration | int64       | <NA>          |
| version                   | int64       | <NA>          |
| line                      | int64       | <NA>          |
| roi                       | int64       | <NA>          |
| index_in_line             | int64       | <NA>          |
| original_fixation_index   | int64       | <NA>          |
| is_fixation_adjusted      | bool        | <NA>          |
| reader_id                 | int64       | <NA>          |
| text_id                   | object      | <NA>          |
| word_index_in_text        | int64       | <NA>          |
| sent_index_in_text        | int64       | <NA>          |
| char_index_in_text        | int64       | <NA>          |
| word                      | object      | <NA>          |
| character                 | object      | <NA>          |

[Merged: reading measures + word features](./eyetracking_data/reader_rm_wf)

| Column                                                    | Data type   | Description   |
|:----------------------------------------------------------|:------------|:--------------|
| word_index_in_text                                        | int64       | <NA>          |
| word                                                      | object      | <NA>          |
| is_technical_term                                         | int64       | <NA>          |
| is_abbreviation                                           | int64       | <NA>          |
| word_index_in_sent                                        | int64       | <NA>          |
| sent_index_in_text                                        | int64       | <NA>          |
| word_length                                               | int64       | <NA>          |
| is_in_quote                                               | int64       | <NA>          |
| is_in_parentheses                                         | int64       | <NA>          |
| contains_symbol                                           | int64       | <NA>          |
| contains_hyphen                                           | int64       | <NA>          |
| is_clause_beginning                                       | int64       | <NA>          |
| is_sent_beginning                                         | int64       | <NA>          |
| contains_abbreviation                                     | int64       | <NA>          |
| PRELS                                                     | int64       | <NA>          |
| PRELAT                                                    | int64       | <NA>          |
| PPOSAT                                                    | int64       | <NA>          |
| PPER                                                      | int64       | <NA>          |
| PPOSS                                                     | int64       | <NA>          |
| PIDAT                                                     | int64       | <NA>          |
| PIAT                                                      | int64       | <NA>          |
| PIS                                                       | int64       | <NA>          |
| PDAT                                                      | int64       | <NA>          |
| PDS                                                       | int64       | <NA>          |
| NN                                                        | int64       | <NA>          |
| NE                                                        | int64       | <NA>          |
| KOKOM                                                     | int64       | <NA>          |
| KON                                                       | int64       | <NA>          |
| KOUS                                                      | int64       | <NA>          |
| KOUI                                                      | int64       | <NA>          |
| ITJ                                                       | int64       | <NA>          |
| FM                                                        | int64       | <NA>          |
| CARD                                                      | int64       | <NA>          |
| ART                                                       | int64       | <NA>          |
| APZR                                                      | int64       | <NA>          |
| APPO                                                      | int64       | <NA>          |
| APPRART                                                   | int64       | <NA>          |
| APPR                                                      | int64       | <NA>          |
| ADV                                                       | int64       | <NA>          |
| ADJD                                                      | int64       | <NA>          |
| ADJA                                                      | int64       | <NA>          |
| XY                                                        | int64       | <NA>          |
| VMPP                                                      | int64       | <NA>          |
| VMINF                                                     | int64       | <NA>          |
| VMFIN                                                     | int64       | <NA>          |
| VAPP                                                      | int64       | <NA>          |
| VAFIN                                                     | int64       | <NA>          |
| VVPP                                                      | int64       | <NA>          |
| VVIZU                                                     | int64       | <NA>          |
| VVINF                                                     | int64       | <NA>          |
| VVIMP                                                     | int64       | <NA>          |
| VVFIN                                                     | int64       | <NA>          |
| TRUNC                                                     | int64       | <NA>          |
| PTKA                                                      | int64       | <NA>          |
| PTKANT                                                    | int64       | <NA>          |
| PTKVZ                                                     | int64       | <NA>          |
| PTKNEG                                                    | int64       | <NA>          |
| PTKZU                                                     | int64       | <NA>          |
| PAV                                                       | int64       | <NA>          |
| PWAV                                                      | int64       | <NA>          |
| PWAT                                                      | int64       | <NA>          |
| PWS                                                       | int64       | <NA>          |
| PRF                                                       | int64       | <NA>          |
| type                                                      | object      | <NA>          |
| lemma                                                     | object      | <NA>          |
| lemma_length_chars                                        | object      | <NA>          |
| type_length_syllables                                     | float64     | <NA>          |
| annotated_type_frequency_normalized                       | float64     | <NA>          |
| type_frequency_normalized                                 | float64     | <NA>          |
| lemma_frequency_normalized                                | float64     | <NA>          |
| familiarity_normalized                                    | float64     | <NA>          |
| regularity_normalized                                     | float64     | <NA>          |
| document_frequency_normalized                             | float64     | <NA>          |
| sentence_frequency_normalized                             | float64     | <NA>          |
| cumulative_syllable_corpus_frequency_normalized           | float64     | <NA>          |
| cumulative_syllable_lexicon_frequency_normalized          | float64     | <NA>          |
| cumulative_character_corpus_frequency_normalized          | float64     | <NA>          |
| cumulative_character_lexicon_frequency_normalized         | float64     | <NA>          |
| cumulative_character_bigram_corpus_frequency_normalized   | float64     | <NA>          |
| cumulative_character_bigram_lexicon_frequency_normalized  | float64     | <NA>          |
| cumulative_character_trigram_corpus_frequency_normalized  | float64     | <NA>          |
| cumulative_character_trigram_lexicon_frequency_normalized | float64     | <NA>          |
| initial_letter_frequency_normalized                       | float64     | <NA>          |
| initial_bigram_frequency_normalized                       | float64     | <NA>          |
| initial_trigram_frequency_normalized                      | float64     | <NA>          |
| avg_cond_prob_in_bigrams                                  | float64     | <NA>          |
| avg_cond_prob_in_trigrams                                 | float64     | <NA>          |
| neighbors_coltheart_higher_freq_cum_freq_normalized       | float64     | <NA>          |
| neighbors_coltheart_higher_freq_count_normalized          | float64     | <NA>          |
| neighbors_coltheart_all_cum_freq_normalized               | float64     | <NA>          |
| neighbors_coltheart_all_count_normalized                  | float64     | <NA>          |
| neighbors_levenshtein_higher_freq_cum_freq_normalized     | float64     | <NA>          |
| neighbors_levenshtein_higher_freq_count_normalized        | float64     | <NA>          |
| neighbors_levenshtein_all_cum_freq_normalized             | float64     | <NA>          |
| neighbors_levenshtein_all_count_normalized                | float64     | <NA>          |
| FFD                                                       | int64       | <NA>          |
| SFD                                                       | int64       | <NA>          |
| FD                                                        | int64       | <NA>          |
| FPRT                                                      | int64       | <NA>          |
| FRT                                                       | int64       | <NA>          |
| TFT                                                       | int64       | <NA>          |
| RRT                                                       | int64       | <NA>          |
| RPD_inc                                                   | int64       | <NA>          |
| RPD_exc                                                   | int64       | <NA>          |
| RBRT                                                      | int64       | <NA>          |
| Fix                                                       | int64       | <NA>          |
| FPF                                                       | int64       | <NA>          |
| RR                                                        | int64       | <NA>          |
| FPReg                                                     | int64       | <NA>          |
| TRC_out                                                   | int64       | <NA>          |
| TRC_in                                                    | int64       | <NA>          |
| LP                                                        | int64       | <NA>          |
| SL_in                                                     | int64       | <NA>          |
| SL_out                                                    | int64       | <NA>          |
| acc_bq_1                                                  | float64     | <NA>          |
| acc_bq_2                                                  | float64     | <NA>          |
| acc_bq_3                                                  | float64     | <NA>          |
| acc_tq_1                                                  | float64     | <NA>          |
| acc_tq_2                                                  | float64     | <NA>          |
| acc_tq_3                                                  | float64     | <NA>          |
| mean_acc_tq                                               | float64     | <NA>          |
| mean_acc_bq                                               | float64     | <NA>          |
| topic                                                     | int64       | <NA>          |
| trial                                                     | int64       | <NA>          |
| text_id                                                   | object      | <NA>          |
| reader                                                    | int64       | <NA>          |
| gender                                                    | int64       | <NA>          |
| major                                                     | int64       | <NA>          |
| age                                                       | float64     | <NA>          |
| expert_status                                             | int64       | <NA>          |
| domain_expert_status                                      | int64       | <NA>          |

[Merged: scanpaths + reading measures](./eyetracking_data/scanpaths_reader_rm_wf)

| Column                                                    | Data type   | Description   |
|:----------------------------------------------------------|:------------|:--------------|
| fixation_index                                            | int64       | <NA>          |
| topic                                                     | object      | <NA>          |
| trial                                                     | int64       | <NA>          |
| acc_bq_1                                                  | int64       | <NA>          |
| acc_bq_2                                                  | int64       | <NA>          |
| acc_bq_3                                                  | int64       | <NA>          |
| acc_tq_1                                                  | int64       | <NA>          |
| acc_tq_2                                                  | int64       | <NA>          |
| acc_tq_3                                                  | int64       | <NA>          |
| fixation_duration                                         | int64       | <NA>          |
| next_saccade_duration                                     | int64       | <NA>          |
| previous_saccade_duration                                 | int64       | <NA>          |
| version                                                   | int64       | <NA>          |
| line                                                      | int64       | <NA>          |
| roi                                                       | int64       | <NA>          |
| index_in_line                                             | int64       | <NA>          |
| original_fixation_index                                   | int64       | <NA>          |
| is_fixation_adjusted                                      | bool        | <NA>          |
| reader_id                                                 | int64       | <NA>          |
| text_id                                                   | object      | <NA>          |
| word_index_in_text                                        | int64       | <NA>          |
| sent_index_in_text                                        | int64       | <NA>          |
| char_index_in_text                                        | int64       | <NA>          |
| word                                                      | object      | <NA>          |
| character                                                 | object      | <NA>          |
| is_technical_term                                         | int64       | <NA>          |
| is_abbreviation                                           | int64       | <NA>          |
| word_index_in_sent                                        | int64       | <NA>          |
| word_length                                               | int64       | <NA>          |
| is_in_quote                                               | int64       | <NA>          |
| is_in_parentheses                                         | int64       | <NA>          |
| contains_symbol                                           | int64       | <NA>          |
| contains_hyphen                                           | int64       | <NA>          |
| is_clause_beginning                                       | int64       | <NA>          |
| is_sent_beginning                                         | int64       | <NA>          |
| contains_abbreviation                                     | int64       | <NA>          |
| PRELS                                                     | int64       | <NA>          |
| PRELAT                                                    | int64       | <NA>          |
| PPOSAT                                                    | int64       | <NA>          |
| PPER                                                      | int64       | <NA>          |
| PPOSS                                                     | int64       | <NA>          |
| PIDAT                                                     | int64       | <NA>          |
| PIAT                                                      | int64       | <NA>          |
| PIS                                                       | int64       | <NA>          |
| PDAT                                                      | int64       | <NA>          |
| PDS                                                       | int64       | <NA>          |
| NN                                                        | int64       | <NA>          |
| NE                                                        | int64       | <NA>          |
| KOKOM                                                     | int64       | <NA>          |
| KON                                                       | int64       | <NA>          |
| KOUS                                                      | int64       | <NA>          |
| KOUI                                                      | int64       | <NA>          |
| ITJ                                                       | int64       | <NA>          |
| FM                                                        | int64       | <NA>          |
| CARD                                                      | int64       | <NA>          |
| ART                                                       | int64       | <NA>          |
| APZR                                                      | int64       | <NA>          |
| APPO                                                      | int64       | <NA>          |
| APPRART                                                   | int64       | <NA>          |
| APPR                                                      | int64       | <NA>          |
| ADV                                                       | int64       | <NA>          |
| ADJD                                                      | int64       | <NA>          |
| ADJA                                                      | int64       | <NA>          |
| XY                                                        | int64       | <NA>          |
| VMPP                                                      | int64       | <NA>          |
| VMINF                                                     | int64       | <NA>          |
| VMFIN                                                     | int64       | <NA>          |
| VAPP                                                      | int64       | <NA>          |
| VAFIN                                                     | int64       | <NA>          |
| VVPP                                                      | int64       | <NA>          |
| VVIZU                                                     | int64       | <NA>          |
| VVINF                                                     | int64       | <NA>          |
| VVIMP                                                     | int64       | <NA>          |
| VVFIN                                                     | int64       | <NA>          |
| TRUNC                                                     | int64       | <NA>          |
| PTKA                                                      | int64       | <NA>          |
| PTKANT                                                    | int64       | <NA>          |
| PTKVZ                                                     | int64       | <NA>          |
| PTKNEG                                                    | int64       | <NA>          |
| PTKZU                                                     | int64       | <NA>          |
| PAV                                                       | int64       | <NA>          |
| PWAV                                                      | int64       | <NA>          |
| PWAT                                                      | int64       | <NA>          |
| PWS                                                       | int64       | <NA>          |
| PRF                                                       | int64       | <NA>          |
| type                                                      | object      | <NA>          |
| lemma                                                     | object      | <NA>          |
| lemma_length_chars                                        | object      | <NA>          |
| type_length_syllables                                     | float64     | <NA>          |
| annotated_type_frequency_normalized                       | float64     | <NA>          |
| type_frequency_normalized                                 | float64     | <NA>          |
| lemma_frequency_normalized                                | float64     | <NA>          |
| familiarity_normalized                                    | float64     | <NA>          |
| regularity_normalized                                     | float64     | <NA>          |
| document_frequency_normalized                             | float64     | <NA>          |
| sentence_frequency_normalized                             | float64     | <NA>          |
| cumulative_syllable_corpus_frequency_normalized           | float64     | <NA>          |
| cumulative_syllable_lexicon_frequency_normalized          | float64     | <NA>          |
| cumulative_character_corpus_frequency_normalized          | float64     | <NA>          |
| cumulative_character_lexicon_frequency_normalized         | float64     | <NA>          |
| cumulative_character_bigram_corpus_frequency_normalized   | float64     | <NA>          |
| cumulative_character_bigram_lexicon_frequency_normalized  | float64     | <NA>          |
| cumulative_character_trigram_corpus_frequency_normalized  | float64     | <NA>          |
| cumulative_character_trigram_lexicon_frequency_normalized | float64     | <NA>          |
| initial_letter_frequency_normalized                       | float64     | <NA>          |
| initial_bigram_frequency_normalized                       | float64     | <NA>          |
| initial_trigram_frequency_normalized                      | float64     | <NA>          |
| avg_cond_prob_in_bigrams                                  | float64     | <NA>          |
| avg_cond_prob_in_trigrams                                 | float64     | <NA>          |
| neighbors_coltheart_higher_freq_cum_freq_normalized       | float64     | <NA>          |
| neighbors_coltheart_higher_freq_count_normalized          | float64     | <NA>          |
| neighbors_coltheart_all_cum_freq_normalized               | float64     | <NA>          |
| neighbors_coltheart_all_count_normalized                  | float64     | <NA>          |
| neighbors_levenshtein_higher_freq_cum_freq_normalized     | float64     | <NA>          |
| neighbors_levenshtein_higher_freq_count_normalized        | float64     | <NA>          |
| neighbors_levenshtein_all_cum_freq_normalized             | float64     | <NA>          |
| neighbors_levenshtein_all_count_normalized                | float64     | <NA>          |
| FFD                                                       | int64       | <NA>          |
| SFD                                                       | int64       | <NA>          |
| FD                                                        | int64       | <NA>          |
| FPRT                                                      | int64       | <NA>          |
| FRT                                                       | int64       | <NA>          |
| TFT                                                       | int64       | <NA>          |
| RRT                                                       | int64       | <NA>          |
| RPD_inc                                                   | int64       | <NA>          |
| RPD_exc                                                   | int64       | <NA>          |
| RBRT                                                      | int64       | <NA>          |
| Fix                                                       | int64       | <NA>          |
| FPF                                                       | int64       | <NA>          |
| RR                                                        | int64       | <NA>          |
| FPReg                                                     | int64       | <NA>          |
| TRC_out                                                   | int64       | <NA>          |
| TRC_in                                                    | int64       | <NA>          |
| LP                                                        | int64       | <NA>          |
| SL_in                                                     | int64       | <NA>          |
| SL_out                                                    | int64       | <NA>          |
| mean_acc_tq                                               | float64     | <NA>          |
| mean_acc_bq                                               | float64     | <NA>          |
| reader                                                    | int64       | <NA>          |
| gender                                                    | int64       | <NA>          |
| major                                                     | int64       | <NA>          |
| age                                                       | float64     | <NA>          |
| expert_status                                             | int64       | <NA>          |
| domain_expert_status                                      | int64       | <NA>          |


## Participants

[Participants](./participants/participant_data.tsv)

| Column        | Data type   | Description   |
|:--------------|:------------|:--------------|
| reader_id     | int64       | <NA>          |
| major         | object      | <NA>          |
| expert_status | object      | <NA>          |
| glasses       | object      | <NA>          |
| age           | float64     | <NA>          |
| handedness    | object      | <NA>          |
| hours_sleep   | float64     | <NA>          |
| alcohol       | object      | <NA>          |
| gender        | object      | <NA>          |
