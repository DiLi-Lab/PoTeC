# Data annotation




 
## PoS tags and syntactic features
this is directly copied from the paper, should I write here: "more details in the paper" / change the wording / copy directly?
> Each text was manually part-of-speech (PoS) tagged according to the Stuttgart-T\"ubingen-Tagset (STTS) \citep{STTSguidelines}. 
In addition to the PoS-tag of the word itself, we provide the PoS-tag of punctuation marks that directly (i.e., without a white space) 
precede or followed the word, as well as hand-crafted tags to indicate whether a word was contained in a constituent 
that is in quotes or parentheses. Furthermore, the words were manually tagged for other lexical and orthographic 
features that arguably affect eye movement behavior in reading, namely whether the word is a technical term, is 
or contains an abbreviation, contains a non-Latin character or symbol, or contains a hyphen. Finally, we added 
various oridnal or binary tags to encoded positional information for each word (ordinal position of the word in the 
text and in the sentence, whether it is the last word of a clause or sentence, and whether it is preceded or followed 
by punctuation). See Table~\ref{features2} for the precise definitions of the different hand-crafted word-tags. 

| **Feature**                         | **Definition**                                                                                                                                                         |
|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| _Lexical and orthographic features_ |                                                                                                                                                                        |
| technical term                      | codes whether the word is a technical term and for technical terms whether it is commonly used in non-technical contexts or only in technical texts (ternary variable) |
| is abbreviation                     | codes whether the token is an abbreviation                                                                                                                             |
| contains abbreviation               | codes whether the token contains an abbreviation                                                                                                                       |
| symbol                              | word contains a symbol  (e.g., z-Richtung, $+$Ende; $\beta$-D-Glucose)                                                                                                 |
| hyph                                | word contains at least one hyphen that is  \textit{not} STTS-tagged as TRUNC (e.g.,  DNA-Fragment, z-Richtung,  $\beta$-D-Glucose)                                     |
| _Linear position information_       |                                                                                                                                                                        |
| word index in text                  | position of the word within the current text, irrespective of sentences coded as integer                                                                               |
| word index in sentence              | position of the word within the current sentence coded as integer                                                                                                      |
| sentence index                      | position of the sentence to which the word belongs within the current text coded as integer                                                                            |
| _Punctuation_                       |                                                                                                                                                                        |
| STTS punctuation before             | STTS-tag of the punctuation that precedes the word                                                                                                                     |
| STTS punctuation after              | STTS-tag of the punctuation that follows the word                                                                                                                      |
| quote                               | word is (part of an expression that is) in quotes                                                                                                                      |
| parentheses                         | word is (part of an expression that is) in parentheses                                                                                                                 |
| _Syntactic features_                |                                                                                                                                                                        |
| clause begin                        | first word of a new clause                                                                                                                                             |
| sentence begin                      | first word of a sentence                                                                                                                                               |
|                                     |                                                                                                                                                                        |


## Corpus-based features
Same here
> Moreover, for each word, several word length measures, lexical frequency measures, and lexical neighborhood measures 
commonly used in reading research were extracted from the lexical database dlexDB  \citep{dlex, Heister2011}, which is 
based on the reference corpus underlying the  Digital Dictionary of the German Language (DWDS) corpus \citep{dwds}. 
All extracted values were manually corrected by a linguistic expert labeller. In particular, the  %(see \texttt{features.py}). 
 type-to-lemma mapping was disambiguated  and incorrect database entries (e.g., incorrect lemmatization) were, whenever 
possible, corrected and otherwise re-coded as missing values. An overview of all features extracted from dLexDB is 
provided in Table~\ref{table:features1}.

| Feature                                                           | Definition                                                                                                                                                                             |
|-------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| _Linguistic representations_                                                                                                                                                                                                                                |
| Type                                                              | Orthographical Representation Of A Word As Found In The Corpus                                                                                                                         |
| Lemma                                                             | Headword, I.e., An Uninflected Form That May Or May Not Occur In The Corpus Itself                                                                                                     |
| Syllables                                                         | Syllables Of Which The Word Consists                                                                                                                                                   |
| _Word length measures_                                              |                                                                                                                                                                                        |
| Type Length (number Of Characters)                                | Number Of Characters Of A Type                                                                                                                                                         |
| Type Length (number Of Syllables)                                 | Number Of Syllables Of A Type                                                                                                                                                          |
| Lemma Length (number Of Characters)                               | Number Of Characters Of A Lemma                                                                                                                                                        |
| _Frequency measures_                                                |                                                                                                                                                                                        |
| Annotated Type Frequency                                          | Number Of Occurrences Of A  Unique Combination Of A Type, Its Stts Tag And Its Lemma  In The Corpus (per Mio Tokens)                                                                   |
| Type Frequency                                                    | Number Of Occurrences Of A Type In The Corpus (per Mio Tokens)                                                                                                                         |
| Lemma Frequency                                                   | Total Number Of Occurrences Of Types Associated With This Lemma In The Corpus (per Mio Tokens)                                                                                         |
| Document Frequency                                                | The Number Of Documents With At Least One Occurrence Of This Type (per 10.000 Documents)                                                                                               |
| Sentence Frequency                                                | Number Of Sentences With At Least One Occurrence Of This Type (per 100.000 Sentences)                                                                                                  |
| Cumulative Syllable Corpus Frequency                              | Number Of Occurrences In The Syllabified Representation Of The Corpus (per Mio Tokens)                                                                                                 |
| Cumulative Syllable Lexicon Frequency                             | Number Of Occurrences In The Syllabified List Of Types (per Mio Types)                                                                                                                 |
| Cumulative Character Corpus Frequency                             | Cumulative Corpus Frequency Of All Characters Contained In This Type (per Mio Tokens)                                                                                                  |
| Cumulative Character Lexicon Frequency                            | Cumulative Lexicon Frequency Of All Characters Contained In This Type (per Mio Types)                                                                                                  |
| Cumulative Character Bigram Corpus Frequency                      | Cumulative Corpus Frequency Of All Character Bigrams Contained In This Type (per Mio Tokens)                                                                                           |
| Cumulative Character Bigram Lexicon Frequency                     | Cumulative Lexicon Frequency Of All Character Bigrams Contained In This Type  (per Mio Types)                                                                                          |
| Cumulative Character Trigram Corpus Frequency                     | Cumulative Corpus Frequency Of All Character Trigrams Contained In This Type  (per Mio Tokens)                                                                                         |
| Cumulative Character Trigram Lexicon Frequency                    | Cumulative Lexicon Frequency Of All Character Trigrams Contained In This Type  (per Mio Types)                                                                                         |
| Initial Letter Frequency                                          | Cumulative Frequency Of All Types Sharing The Same Initial Letter (per Mio Tokens)                                                                                                     |
| Initial Bigram Frequency                                          | Cumulative Frequency Of All Types Sharing The Same Initial Character Bigram (per Mio Tokens)                                                                                           |
| Initial Trigram Frequency                                         | Cumulative Frequency Of All Types Sharing The Same Initial Character Trigram (per Mio Tokens)                                                                                          |
| Average Conditional Probability (in Bigrams)                      | Conditional Probability Of The Bigram, Given The Occurrence Of Its First Component, Averaged Across All Character Positions (computed On The Basis Of The Annotated Type Information)  |
| Average Conditional Probability  (in Trigrams)                    | Conditional Probability Of The Trigram, Given The Occurrence Of Its First Component, Averaged Across All Character Positions (computed On The Basis Of The Annotated Type Information) |
| Familiarity                                                       | Cumulative Frequency Of All Types Of The Same Length Sharing The Same Initial Trigram                                                                                                  |
| Regularity                                                        | The Number Of Types Of The Same Length Sharing The Same Initial Trigram                                                                                                                |
| _Neighborhood measures_                                             |                                                                                                                                                                                        |
| Cumulative Frequency Of Higher Frequency Neighbors (coltheart)    | Cumulative Frequency Of All Higher Frequency Orthographic Neighbors According To The Definition Of \citep{coltheart1977}                                                               |
| Count Of Of Higher Frequency Neighbors                            | Number Of Higher Frequency Orthographic Neighbors According To The Definition Of \citep{coltheart1977}                                                                                 |
| Cumulative Frequency Of All Neighbors (coltheart)                 | Cumulative Frequency Of All Orthographic Neighbors According To The Definition Of \citep{coltheart1977}                                                                                |
| Count Of All Neighbors (coltheart)                                | Number Of Orthographic Neighbors According To The Definition Of \citep{coltheart1977}                                                                                                  |
| Cumulative Frequency Of Higher Frequency Neighbors  (levenshtein) | Cumulative Frequency Of All Higher Frequency Orthographic Neighbors According To The Definition Of \citep{levenshtein1966}                                                             |
| Count Of Of Higher Frequency Neighbors (levenshtein)              | Number Of Higher Frequency Orthographic Neighbors According To The Definition Of \citep{levenshtein1966}                                                                               |
| Cumulative Frequency Of All Neighbors (levenshtein)               | Cumulative Frequency Of All Orthographic Neighbors According To The Definition Of \citep{levenshtein1966}                                                                              |
| Count Of All Neighbors (levenshtein)                              | Number Of Orthographic Neighbors According To The Definition Of  \citep{levenshtein1966}                                                                                               |
|                                                                   |                                                                                                                                                                                        |
