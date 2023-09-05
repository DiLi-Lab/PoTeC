# Data annotation process

All stimuli texts were annotated with corpus based and syntactic features, but also lexical and orthographic features.
A short description of all annotation tags can be found in the [CODEBOOK.md](CODEBOOK.md) while the decision 
process and more detailed descriptions of manual tags is explained in more detail in the following sections.

## Manual annotation
All text were manually PoS-tagged according to the Suttgart-Tübingen-Tagset 
(Schiller et al. (1999), [STTS](http://www.sfs.uni-tuebingen.de/resources/stts-1999.pdf)).

### Hand-crafted tags
In addition to the standard STTS tags, the following tags were added manually. Those tags reflect features of words 
that are important for studying eye-movements and that might show an effect on eye-movements. 

* **Technical term**: This feature is used to tag two types of technical terms: the first enocdes whether the word is a technical term
that is generally understandable for a layperson (e.g. "DNA") and the second whether the word is a technical term that is only
understandable for a domain expert (e.g. "DNA-Strang").
* **Abbreviation**: If the word is an abbreviation and does not contain other word parts, e.g. "DNA". 
* **Contains abbreviation**: Words that contain an abbreviation, e.g. "DNA-Strang" contains the abbreviation "DNA".
* **Punctuation _before_ the word**: The tags of the punctuation mark(s) (can be more than one) that directly 
_precede_ the current word. If there is no punctuation mark before the word, the tag is "NA".
* **Punctuation _after_ the word**: The tags of the punctuation mark(s) (can be more than one) that directly 
_follow_ the current word. If there is no punctuation mark after the word, the tag is "NA".
* **Quote**: if the word is part of a quote
* **Parentheses**: if the word is part of an expression in parentheses
* **Symbol**: if the word contains a symbol (e.g. "+Ende" contains the symbol "+") or other non-latin character
* **Hyphen**: if the word contains a hyphen (e.g. "DNA-Strang")
* **Clause beginning**: if the word is the first word of a clause
* **Sentence beginning**: if the word is the first word of a sentence
* word index in text
* word index in sentence



## DlexDB annotations
Moreover, for each word, several word length measures, lexical frequency measures, and lexical neighborhood measures 
commonly used in reading research were extracted from the lexical database dlexDB  \citep{dlex, Heister2011}, which is 
based on the reference corpus underlying the  Digital Dictionary of the German Language (DWDS) corpus \citep{dwds}. 
All extracted values were manually corrected by a linguistic expert labeller. In particular, the  %(see \texttt{features.py}). 
 type-to-lemma mapping was disambiguated  and incorrect database entries (e.g., incorrect lemmatization) were, whenever 
possible, corrected and otherwise re-coded as missing values.

### Manual correction

A few annotations needed manual correction either because they were wrong / missing or a different annotation was more 
appropriate for an eye-tracking corpus.
 * **Abbreviation syllables**: Type length in syllables were mostly 1 for abbreviations. The annotation of those words was corrected to reflect the pronunciation 
of the abbreviation (e.g. "DNA" has 3 syllables: "D-N-A")
 * **Remove annotated type frequency**: Some words have too many PoS-tags in the database (e.g. "Mikrotubuli"). The annotated type frequency was 
set to "None" for those words. The same is true for types with too many wrong tags.
 * **Add lemma frequency**: If there was a lemma but not type, the lemma frequency was added.
 * **Wrong PoS-tags**: if the PoS-tag was very clearly wrong, it was corrected (e.g. "Dimer" was tagged as "PIS" instead of "NN"). 
Also, as all words have previously been manually tagged, both tags were compared. If there was a mismatch, the tag was corrected.
 * **No entry**: For words without entry in the dlexDB, the lemma, lemma length, syllables and type length in syllables were added manually.
 * **Wrong lemma**: If the lemma was wrong, it was manually corrected if possible and else recorded as missing value.


Schiller, A., Teufel, S., Stöckert, C. (1999). Guidelines f ̈ur das Tagging
deutscher Textcorpora mit STTS (Kleines und großes Tagset). www.sfs.uni-tuebingen.de/resources/stts-1999.pdf.

