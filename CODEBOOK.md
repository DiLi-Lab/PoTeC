# Codebook

## Stimuli

[Word features](./stimuli/word_features)
todos:
- check whether text and word columns are always exactly equal, if yes, delete text, but move word to the first column
- 

| Column                                                     | Data type   | Description   |
|:-----------------------------------------------------------|:------------|:--------------|
| Text                                                       | object      | <NA>          |
| SSTS-Tag                                                   | object      | <NA>          |
| Line                                                       | int64       | <NA>          |
| Word                                                       | object      | <NA>          |
| Type                                                       | object      | <NA>          |
| Type_length_(characters)                                   | int64       | <NA>          |
| PoS_tag                                                    | object      | <NA>          |
| Lemma                                                      | object      | <NA>          |
| Lemma_length_(characters)                                  | int64       | <NA>          |
| Syllables                                                  | object      | <NA>          |
| Type_length_(syllables)                                    | float64     | <NA>          |
| Annotated_type_frequency_normalized                        | float64     | <NA>          |
| Type_frequency_normalized                                  | float64     | <NA>          |
| Lemma_frequency_normalized                                 | float64     | <NA>          |
| Familiarity_normalized                                     | float64     | <NA>          |
| Regularity_normalized                                      | float64     | <NA>          |
| Document_frequency_normalized                              | float64     | <NA>          |
| Sentence_frequency_normalized                              | float64     | <NA>          |
| Cumulative_syllable_corpus_frequency_normalized            | float64     | <NA>          |
| Cumulative_syllable_lexicon_frequency_normalized           | float64     | <NA>          |
| Cumulative_character_corpus_frequency_normalized           | float64     | <NA>          |
| Cumulative_character_lexicon_frequency_normalized          | float64     | <NA>          |
| Cumulative_character_bigram_corpus_frequency_normalized    | float64     | <NA>          |
| Cumulative_character_bigram_lexicon_frequency_normalized   | float64     | <NA>          |
| Cumulative_character_trigram_corpus_frequency_normalized   | float64     | <NA>          |
| Cumulative_character_trigram_lexicon_frequency_normalized  | float64     | <NA>          |
| Initial_letter_frequency_normalized                        | float64     | <NA>          |
| Initial_bigram_frequency_normalized                        | float64     | <NA>          |
| Initial_trigram_frequency_normalized                       | float64     | <NA>          |
| Avg._cond._prob.,_in_bigrams                               | float64     | <NA>          |
| Avg._cond._prob.,_in_trigrams                              | float64     | <NA>          |
| Neighbors_Coltheart_higher_freq.,_cum._freq.,_normalized   | float64     | <NA>          |
| Neighbors_Coltheart_higher_freq.,_count,_normalized        | float64     | <NA>          |
| Neighbors_Coltheart_all,_cum._freq.,_normalized            | float64     | <NA>          |
| Neighbors_Coltheart_all,_count,_normalized                 | float64     | <NA>          |
| Neighbors_Levenshtein_higher_freq.,_cum._freq.,_normalized | float64     | <NA>          |
| Neighbors_Levenshtein_higher_freq.,_count,_normalized      | float64     | <NA>          |
| Neighbors_Levenshtein_all,_cum._freq.,_normalized          | float64     | <NA>          |
| Neighbors_Levenshtein_all,_count,_normalized               | float64     | <NA>          |

[Text tags](./stimuli/text_tags)

| Column                 | Data type   | Description   |
|:-----------------------|:------------|:--------------|
| WORD_INDEX             | int64       | <NA>          |
| WORD                   | object      | <NA>          |
| STTS_PoSTag            | object      | <NA>          |
| TechnialTerm           | int64       | <NA>          |
| Abbreviation           | int64       | <NA>          |
| WordIndexInSentence    | int64       | <NA>          |
| SentenceIndex          | int64       | <NA>          |
| WordLen                | int64       | <NA>          |
| STTS_Punctuationbefore | float64     | <NA>          |
| STTS_Punctuationafter  | object      | <NA>          |
| Position               | object      | <NA>          |
| WordIndexInText        | int64       | <NA>          |
| textID                 | object      | <NA>          |
| Quote                  | int64       | <NA>          |
| Parentheses            | int64       | <NA>          |
| Symbol                 | int64       | <NA>          |
| Hyph                   | int64       | <NA>          |
| ClauseBegin            | int64       | <NA>          |
| SentenceBegin          | int64       | <NA>          |
| isAbbr                 | int64       | <NA>          |
| containsAbbr           | int64       | <NA>          |
| PRELS                  | int64       | <NA>          |
| PRELAT                 | int64       | <NA>          |
| PPOSAT                 | int64       | <NA>          |
| PPER                   | int64       | <NA>          |
| PPOSS                  | int64       | <NA>          |
| PIDAT                  | int64       | <NA>          |
| PIAT                   | int64       | <NA>          |
| PIS                    | int64       | <NA>          |
| PDAT                   | int64       | <NA>          |
| PDS                    | int64       | <NA>          |
| NN                     | int64       | <NA>          |
| NE                     | int64       | <NA>          |
| KOKOM                  | int64       | <NA>          |
| KON                    | int64       | <NA>          |
| KOUS                   | int64       | <NA>          |
| KOUI                   | int64       | <NA>          |
| ITJ                    | int64       | <NA>          |
| FM                     | int64       | <NA>          |
| CARD                   | int64       | <NA>          |
| ART                    | int64       | <NA>          |
| APZR                   | int64       | <NA>          |
| APPO                   | int64       | <NA>          |
| APPRART                | int64       | <NA>          |
| APPR                   | int64       | <NA>          |
| ADV                    | int64       | <NA>          |
| ADJD                   | int64       | <NA>          |
| ADJA                   | int64       | <NA>          |
| XY                     | int64       | <NA>          |
| VMPP                   | int64       | <NA>          |
| VMINF                  | int64       | <NA>          |
| VMFIN                  | int64       | <NA>          |
| VAPP                   | int64       | <NA>          |
| VAFIN                  | int64       | <NA>          |
| VVPP                   | int64       | <NA>          |
| VVIZU                  | int64       | <NA>          |
| VVINF                  | int64       | <NA>          |
| VVIMP                  | int64       | <NA>          |
| VVFIN                  | int64       | <NA>          |
| TRUNC                  | int64       | <NA>          |
| PTKA                   | int64       | <NA>          |
| PTKANT                 | int64       | <NA>          |
| PTKVZ                  | int64       | <NA>          |
| PTKNEG                 | int64       | <NA>          |
| PTKZU                  | int64       | <NA>          |
| PAV                    | int64       | <NA>          |
| PWAV                   | int64       | <NA>          |
| PWAT                   | int64       | <NA>          |
| PWS                    | int64       | <NA>          |
| PRF                    | int64       | <NA>          |

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

| Column                     | Data types   | Decscription   |
|:---------------------------|:-------------|:---------------|
| CURRENT_FIX_INDEX          | int64        | <NA>           |
| topic                      | object       | <NA>           |
| trial                      | int64        | <NA>           |
| ACC_B_Q1                   | int64        | <NA>           |
| ACC_B_Q2                   | int64        | <NA>           |
| ACC_B_Q3                   | int64        | <NA>           |
| ACC_T_Q1                   | int64        | <NA>           |
| ACC_T_Q2                   | int64        | <NA>           |
| ACC_T_Q3                   | int64        | <NA>           |
| CURRENT_FIX_DURATION       | int64        | <NA>           |
| NEXT_SAC_DURATION          | int64        | <NA>           |
| PREVIOUS_SAC_DURATION      | object       | <NA>           |
| version                    | int64        | <NA>           |
| line                       | int64        | <NA>           |
| roi                        | int64        | <NA>           |
| index_inline               | int64        | <NA>           |
| ORIGINAL_CURRENT_FIX_INDEX | int64        | <NA>           |
| Fix_adjusted               | bool         | <NA>           |
| RECORDING_SESSION_LABEL    | int64        | <NA>           |
| itemid                     | object       | <NA>           |


[Reading measures](./eyetracking_data/reading_measures)

| Column        | Data type   | Description   |
|:--------------|:------------|:--------------|
| WordIndexSent | int64       | <NA>          |
| SentIndex     | int64       | <NA>          |
| FFD           | int64       | <NA>          |
| SFD           | int64       | <NA>          |
| FD            | int64       | <NA>          |
| FPRT          | int64       | <NA>          |
| FRT           | int64       | <NA>          |
| TFT           | int64       | <NA>          |
| RRT           | int64       | <NA>          |
| RPD_inc       | int64       | <NA>          |
| RPD_exc       | int64       | <NA>          |
| RBRT          | int64       | <NA>          |
| Fix           | int64       | <NA>          |
| FPF           | int64       | <NA>          |
| RR            | int64       | <NA>          |
| FPReg         | int64       | <NA>          |
| TRC_out       | int64       | <NA>          |
| TRC_in        | int64       | <NA>          |
| LP            | int64       | <NA>          |
| SL_in         | int64       | <NA>          |
| SL_out        | int64       | <NA>          |
| ACC_B_Q1      | float64     | <NA>          |
| ACC_B_Q2      | float64     | <NA>          |
| ACC_B_Q3      | float64     | <NA>          |
| ACC_T_Q1      | float64     | <NA>          |
| ACC_T_Q2      | float64     | <NA>          |
| ACC_T_Q3      | float64     | <NA>          |
| topic         | int64       | <NA>          |
| trial         | int64       | <NA>          |
| itemid        | object      | <NA>          |
| reader        | int64       | <NA>          |
| gender        | int64       | <NA>          |
| major         | int64       | <NA>          |
| expert_status | int64       | <NA>          |
| age           | float64     | <NA>          |
| meanAccBQ     | float64     | <NA>          |
| meanAccTQ     | float64     | <NA>          |
| group         | int64       | <NA>          |

[Scanpaths](./eyetracking_data/scanpaths)

| Column                     | Data type   | Description   |
|:---------------------------|:------------|:--------------|
| CURRENT_FIX_INDEX          | int64       | <NA>          |
| topic                      | object      | <NA>          |
| trial                      | int64       | <NA>          |
| ACC_B_Q1                   | int64       | <NA>          |
| ACC_B_Q2                   | int64       | <NA>          |
| ACC_B_Q3                   | int64       | <NA>          |
| ACC_T_Q1                   | int64       | <NA>          |
| ACC_T_Q2                   | int64       | <NA>          |
| ACC_T_Q3                   | int64       | <NA>          |
| CURRENT_FIX_DURATION       | int64       | <NA>          |
| NEXT_SAC_DURATION          | int64       | <NA>          |
| PREVIOUS_SAC_DURATION      | int64       | <NA>          |
| version                    | int64       | <NA>          |
| line                       | int64       | <NA>          |
| roi                        | int64       | <NA>          |
| index_inline               | int64       | <NA>          |
| ORIGINAL_CURRENT_FIX_INDEX | int64       | <NA>          |
| Fix_adjusted               | bool        | <NA>          |
| RECORDING_SESSION_LABEL    | int64       | <NA>          |
| itemid                     | object      | <NA>          |
| wordIndexInText            | int64       | <NA>          |
| sentIndex                  | int64       | <NA>          |
| charIndexInText            | int64       | <NA>          |
| word                       | object      | <NA>          |
| character                  | object      | <NA>          |

[Merged: reading measures + word features](./eyetracking_data/reader_rm_wf)

| Column                                                     | Data type   | Description   |
|:-----------------------------------------------------------|:------------|:--------------|
| WORD                                                       | object      | <NA>          |
| TechnialTerm                                               | int64       | <NA>          |
| WordIndexInSentence                                        | int64       | <NA>          |
| SentenceIndex                                              | int64       | <NA>          |
| WordLen                                                    | int64       | <NA>          |
| WordIndexInText                                            | int64       | <NA>          |
| Quote                                                      | int64       | <NA>          |
| Parentheses                                                | int64       | <NA>          |
| Symbol                                                     | int64       | <NA>          |
| Hyph                                                       | int64       | <NA>          |
| ClauseBegin                                                | int64       | <NA>          |
| SentenceBegin                                              | int64       | <NA>          |
| isAbbr                                                     | int64       | <NA>          |
| containsAbbr                                               | int64       | <NA>          |
| PRELS                                                      | int64       | <NA>          |
| PRELAT                                                     | int64       | <NA>          |
| PPOSAT                                                     | int64       | <NA>          |
| PPER                                                       | int64       | <NA>          |
| PPOSS                                                      | int64       | <NA>          |
| PIDAT                                                      | int64       | <NA>          |
| PIAT                                                       | int64       | <NA>          |
| PIS                                                        | int64       | <NA>          |
| PDAT                                                       | int64       | <NA>          |
| PDS                                                        | int64       | <NA>          |
| NN                                                         | int64       | <NA>          |
| NE                                                         | int64       | <NA>          |
| KOKOM                                                      | int64       | <NA>          |
| KON                                                        | int64       | <NA>          |
| KOUS                                                       | int64       | <NA>          |
| KOUI                                                       | int64       | <NA>          |
| ITJ                                                        | int64       | <NA>          |
| FM                                                         | int64       | <NA>          |
| CARD                                                       | int64       | <NA>          |
| ART                                                        | int64       | <NA>          |
| APZR                                                       | int64       | <NA>          |
| APPO                                                       | int64       | <NA>          |
| APPRART                                                    | int64       | <NA>          |
| APPR                                                       | int64       | <NA>          |
| ADV                                                        | int64       | <NA>          |
| ADJD                                                       | int64       | <NA>          |
| ADJA                                                       | int64       | <NA>          |
| XY                                                         | int64       | <NA>          |
| VMPP                                                       | int64       | <NA>          |
| VMINF                                                      | int64       | <NA>          |
| VMFIN                                                      | int64       | <NA>          |
| VAPP                                                       | int64       | <NA>          |
| VAFIN                                                      | int64       | <NA>          |
| VVPP                                                       | int64       | <NA>          |
| VVIZU                                                      | int64       | <NA>          |
| VVINF                                                      | int64       | <NA>          |
| VVIMP                                                      | int64       | <NA>          |
| VVFIN                                                      | int64       | <NA>          |
| TRUNC                                                      | int64       | <NA>          |
| PTKA                                                       | int64       | <NA>          |
| PTKANT                                                     | int64       | <NA>          |
| PTKVZ                                                      | int64       | <NA>          |
| PTKNEG                                                     | int64       | <NA>          |
| PTKZU                                                      | int64       | <NA>          |
| PAV                                                        | int64       | <NA>          |
| PWAV                                                       | int64       | <NA>          |
| PWAT                                                       | int64       | <NA>          |
| PWS                                                        | int64       | <NA>          |
| PRF                                                        | int64       | <NA>          |
| Type                                                       | object      | <NA>          |
| Lemma                                                      | object      | <NA>          |
| Lemma_length_(characters)                                  | float64     | <NA>          |
| Type_length_(syllables)                                    | float64     | <NA>          |
| Annotated_type_frequency_normalized                        | float64     | <NA>          |
| Type_frequency_normalized                                  | float64     | <NA>          |
| Lemma_frequency_normalized                                 | float64     | <NA>          |
| Familiarity_normalized                                     | float64     | <NA>          |
| Regularity_normalized                                      | float64     | <NA>          |
| Document_frequency_normalized                              | float64     | <NA>          |
| Sentence_frequency_normalized                              | float64     | <NA>          |
| Cumulative_syllable_corpus_frequency_normalized            | float64     | <NA>          |
| Cumulative_syllable_lexicon_frequency_normalized           | float64     | <NA>          |
| Cumulative_character_corpus_frequency_normalized           | float64     | <NA>          |
| Cumulative_character_lexicon_frequency_normalized          | float64     | <NA>          |
| Cumulative_character_bigram_corpus_frequency_normalized    | float64     | <NA>          |
| Cumulative_character_bigram_lexicon_frequency_normalized   | float64     | <NA>          |
| Cumulative_character_trigram_corpus_frequency_normalized   | float64     | <NA>          |
| Cumulative_character_trigram_lexicon_frequency_normalized  | float64     | <NA>          |
| Initial_letter_frequency_normalized                        | float64     | <NA>          |
| Initial_bigram_frequency_normalized                        | float64     | <NA>          |
| Initial_trigram_frequency_normalized                       | float64     | <NA>          |
| Avg._cond._prob.,_in_bigrams                               | float64     | <NA>          |
| Avg._cond._prob.,_in_trigrams                              | float64     | <NA>          |
| Neighbors_Coltheart_higher_freq.,_cum._freq.,_normalized   | float64     | <NA>          |
| Neighbors_Coltheart_higher_freq.,_count,_normalized        | float64     | <NA>          |
| Neighbors_Coltheart_all,_cum._freq.,_normalized            | float64     | <NA>          |
| Neighbors_Coltheart_all,_count,_normalized                 | float64     | <NA>          |
| Neighbors_Levenshtein_higher_freq.,_cum._freq.,_normalized | float64     | <NA>          |
| Neighbors_Levenshtein_higher_freq.,_count,_normalized      | float64     | <NA>          |
| Neighbors_Levenshtein_all,_cum._freq.,_normalized          | float64     | <NA>          |
| Neighbors_Levenshtein_all,_count,_normalized               | float64     | <NA>          |
| WordIndexSent                                              | int64       | <NA>          |
| SentIndex                                                  | int64       | <NA>          |
| FFD                                                        | int64       | <NA>          |
| SFD                                                        | int64       | <NA>          |
| FD                                                         | int64       | <NA>          |
| FPRT                                                       | int64       | <NA>          |
| FRT                                                        | int64       | <NA>          |
| TFT                                                        | int64       | <NA>          |
| RRT                                                        | int64       | <NA>          |
| RPD_inc                                                    | int64       | <NA>          |
| RPD_exc                                                    | int64       | <NA>          |
| RBRT                                                       | int64       | <NA>          |
| Fix                                                        | int64       | <NA>          |
| FPF                                                        | int64       | <NA>          |
| RR                                                         | int64       | <NA>          |
| FPReg                                                      | int64       | <NA>          |
| TRC_out                                                    | int64       | <NA>          |
| TRC_in                                                     | int64       | <NA>          |
| LP                                                         | int64       | <NA>          |
| SL_in                                                      | int64       | <NA>          |
| SL_out                                                     | int64       | <NA>          |
| ACC_B_Q1                                                   | float64     | <NA>          |
| ACC_B_Q2                                                   | float64     | <NA>          |
| ACC_B_Q3                                                   | float64     | <NA>          |
| ACC_T_Q1                                                   | float64     | <NA>          |
| ACC_T_Q2                                                   | float64     | <NA>          |
| ACC_T_Q3                                                   | float64     | <NA>          |
| meanAccTQ                                                  | float64     | <NA>          |
| meanAccBQ                                                  | float64     | <NA>          |
| topic                                                      | int64       | <NA>          |
| trial                                                      | int64       | <NA>          |
| itemid                                                     | object      | <NA>          |
| reader                                                     | int64       | <NA>          |
| gender                                                     | int64       | <NA>          |
| major                                                      | int64       | <NA>          |
| expert_status                                              | int64       | <NA>          |
| age                                                        | float64     | <NA>          |
| group                                                      | int64       | <NA>          |

[Merged: scanpaths + reading measures](./eyetracking_data/scanpaths_reader_rm_wf)

| Column                                                     | Data type   | Description   |
|:-----------------------------------------------------------|:------------|:--------------|
| CURRENT_FIX_INDEX                                          | int64       | <NA>          |
| topic                                                      | object      | <NA>          |
| trial                                                      | int64       | <NA>          |
| ACC_B_Q1                                                   | int64       | <NA>          |
| ACC_B_Q2                                                   | int64       | <NA>          |
| ACC_B_Q3                                                   | int64       | <NA>          |
| ACC_T_Q1                                                   | int64       | <NA>          |
| ACC_T_Q2                                                   | int64       | <NA>          |
| ACC_T_Q3                                                   | int64       | <NA>          |
| CURRENT_FIX_DURATION                                       | int64       | <NA>          |
| NEXT_SAC_DURATION                                          | int64       | <NA>          |
| PREVIOUS_SAC_DURATION                                      | int64       | <NA>          |
| version                                                    | int64       | <NA>          |
| line                                                       | int64       | <NA>          |
| roi                                                        | int64       | <NA>          |
| index_inline                                               | int64       | <NA>          |
| ORIGINAL_CURRENT_FIX_INDEX                                 | int64       | <NA>          |
| Fix_adjusted                                               | bool        | <NA>          |
| RECORDING_SESSION_LABEL                                    | int64       | <NA>          |
| itemid                                                     | object      | <NA>          |
| wordIndexInText                                            | int64       | <NA>          |
| sentIndex                                                  | int64       | <NA>          |
| charIndexInText                                            | int64       | <NA>          |
| word                                                       | object      | <NA>          |
| character                                                  | object      | <NA>          |
| WORD                                                       | object      | <NA>          |
| TechnialTerm                                               | int64       | <NA>          |
| WordIndexInSentence                                        | int64       | <NA>          |
| SentenceIndex                                              | int64       | <NA>          |
| WordLen                                                    | int64       | <NA>          |
| WordIndexInText                                            | int64       | <NA>          |
| Quote                                                      | int64       | <NA>          |
| Parentheses                                                | int64       | <NA>          |
| Symbol                                                     | int64       | <NA>          |
| Hyph                                                       | int64       | <NA>          |
| ClauseBegin                                                | int64       | <NA>          |
| SentenceBegin                                              | int64       | <NA>          |
| isAbbr                                                     | int64       | <NA>          |
| containsAbbr                                               | int64       | <NA>          |
| PRELS                                                      | int64       | <NA>          |
| PRELAT                                                     | int64       | <NA>          |
| PPOSAT                                                     | int64       | <NA>          |
| PPER                                                       | int64       | <NA>          |
| PPOSS                                                      | int64       | <NA>          |
| PIDAT                                                      | int64       | <NA>          |
| PIAT                                                       | int64       | <NA>          |
| PIS                                                        | int64       | <NA>          |
| PDAT                                                       | int64       | <NA>          |
| PDS                                                        | int64       | <NA>          |
| NN                                                         | int64       | <NA>          |
| NE                                                         | int64       | <NA>          |
| KOKOM                                                      | int64       | <NA>          |
| KON                                                        | int64       | <NA>          |
| KOUS                                                       | int64       | <NA>          |
| KOUI                                                       | int64       | <NA>          |
| ITJ                                                        | int64       | <NA>          |
| FM                                                         | int64       | <NA>          |
| CARD                                                       | int64       | <NA>          |
| ART                                                        | int64       | <NA>          |
| APZR                                                       | int64       | <NA>          |
| APPO                                                       | int64       | <NA>          |
| APPRART                                                    | int64       | <NA>          |
| APPR                                                       | int64       | <NA>          |
| ADV                                                        | int64       | <NA>          |
| ADJD                                                       | int64       | <NA>          |
| ADJA                                                       | int64       | <NA>          |
| XY                                                         | int64       | <NA>          |
| VMPP                                                       | int64       | <NA>          |
| VMINF                                                      | int64       | <NA>          |
| VMFIN                                                      | int64       | <NA>          |
| VAPP                                                       | int64       | <NA>          |
| VAFIN                                                      | int64       | <NA>          |
| VVPP                                                       | int64       | <NA>          |
| VVIZU                                                      | int64       | <NA>          |
| VVINF                                                      | int64       | <NA>          |
| VVIMP                                                      | int64       | <NA>          |
| VVFIN                                                      | int64       | <NA>          |
| TRUNC                                                      | int64       | <NA>          |
| PTKA                                                       | int64       | <NA>          |
| PTKANT                                                     | int64       | <NA>          |
| PTKVZ                                                      | int64       | <NA>          |
| PTKNEG                                                     | int64       | <NA>          |
| PTKZU                                                      | int64       | <NA>          |
| PAV                                                        | int64       | <NA>          |
| PWAV                                                       | int64       | <NA>          |
| PWAT                                                       | int64       | <NA>          |
| PWS                                                        | int64       | <NA>          |
| PRF                                                        | int64       | <NA>          |
| Type                                                       | object      | <NA>          |
| Lemma                                                      | object      | <NA>          |
| Lemma_length_(characters)                                  | int64       | <NA>          |
| Type_length_(syllables)                                    | int64       | <NA>          |
| Annotated_type_frequency_normalized                        | float64     | <NA>          |
| Type_frequency_normalized                                  | float64     | <NA>          |
| Lemma_frequency_normalized                                 | float64     | <NA>          |
| Familiarity_normalized                                     | float64     | <NA>          |
| Regularity_normalized                                      | float64     | <NA>          |
| Document_frequency_normalized                              | float64     | <NA>          |
| Sentence_frequency_normalized                              | float64     | <NA>          |
| Cumulative_syllable_corpus_frequency_normalized            | float64     | <NA>          |
| Cumulative_syllable_lexicon_frequency_normalized           | float64     | <NA>          |
| Cumulative_character_corpus_frequency_normalized           | float64     | <NA>          |
| Cumulative_character_lexicon_frequency_normalized          | float64     | <NA>          |
| Cumulative_character_bigram_corpus_frequency_normalized    | float64     | <NA>          |
| Cumulative_character_bigram_lexicon_frequency_normalized   | float64     | <NA>          |
| Cumulative_character_trigram_corpus_frequency_normalized   | float64     | <NA>          |
| Cumulative_character_trigram_lexicon_frequency_normalized  | float64     | <NA>          |
| Initial_letter_frequency_normalized                        | float64     | <NA>          |
| Initial_bigram_frequency_normalized                        | float64     | <NA>          |
| Initial_trigram_frequency_normalized                       | float64     | <NA>          |
| Avg._cond._prob.,_in_bigrams                               | float64     | <NA>          |
| Avg._cond._prob.,_in_trigrams                              | float64     | <NA>          |
| Neighbors_Coltheart_higher_freq.,_cum._freq.,_normalized   | float64     | <NA>          |
| Neighbors_Coltheart_higher_freq.,_count,_normalized        | float64     | <NA>          |
| Neighbors_Coltheart_all,_cum._freq.,_normalized            | float64     | <NA>          |
| Neighbors_Coltheart_all,_count,_normalized                 | float64     | <NA>          |
| Neighbors_Levenshtein_higher_freq.,_cum._freq.,_normalized | float64     | <NA>          |
| Neighbors_Levenshtein_higher_freq.,_count,_normalized      | float64     | <NA>          |
| Neighbors_Levenshtein_all,_cum._freq.,_normalized          | float64     | <NA>          |
| Neighbors_Levenshtein_all,_count,_normalized               | float64     | <NA>          |
| WordIndexSent                                              | int64       | <NA>          |
| SentIndex                                                  | int64       | <NA>          |
| FFD                                                        | int64       | <NA>          |
| SFD                                                        | int64       | <NA>          |
| FD                                                         | int64       | <NA>          |
| FPRT                                                       | int64       | <NA>          |
| FRT                                                        | int64       | <NA>          |
| TFT                                                        | int64       | <NA>          |
| RRT                                                        | int64       | <NA>          |
| RPD_inc                                                    | int64       | <NA>          |
| RPD_exc                                                    | int64       | <NA>          |
| RBRT                                                       | int64       | <NA>          |
| Fix                                                        | int64       | <NA>          |
| FPF                                                        | int64       | <NA>          |
| RR                                                         | int64       | <NA>          |
| FPReg                                                      | int64       | <NA>          |
| TRC_out                                                    | int64       | <NA>          |
| TRC_in                                                     | int64       | <NA>          |
| LP                                                         | int64       | <NA>          |
| SL_in                                                      | int64       | <NA>          |
| SL_out                                                     | int64       | <NA>          |
| meanAccTQ                                                  | float64     | <NA>          |
| meanAccBQ                                                  | float64     | <NA>          |
| reader                                                     | int64       | <NA>          |
| gender                                                     | int64       | <NA>          |
| major                                                      | int64       | <NA>          |
| expert_status                                              | int64       | <NA>          |
| age                                                        | float64     | <NA>          |
| group                                                      | int64       | <NA>          |


## Participants

[Participants](./participants/participant_data.csv)

| Column          | Data type   | Description   |
|:----------------|:------------|:--------------|
| readerId        | int64       | <NA>          |
| major           | object      | <NA>          |
| beginner/expert | object      | <NA>          |
| glasses         | object      | <NA>          |
| age             | float64     | <NA>          |
| handedness      | object      | <NA>          |
| hours_sleep     | float64     | <NA>          |
| alcohol         | object      | <NA>          |
| gender          | object      | <NA>          |
