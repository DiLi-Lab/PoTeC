# PoTeC - Potsdam Textbook Corpus

This repository contains Potsdam Textbook Corpus (PoTeC) which is a natural reading eye-tracking corpus.
Four groups of participants (advanced/beginner level students of physics and biology) read 12 short 
texts taken from textbooks of physics and biology while their eye movements were monitored. 
The final dataset contains the reading data for 75 participants each reading all 12 texts.
The study follows a 2x2 fully-crossed factorial design:
* _Factor 1_: Study major with the levels either physics or biology
* _Factor 2_: Level of expertise with the levels either beginner or advanced

|              | Physics | Biology |
|--------------|---------|---------|
| **Beginner** | 12      | 16      |
| **Advanced** | 20      | 27      |

Both factors are quasi-experimental and manipulated between subjects.
The readers' text comprehension as well as their background 
knowledge in the topics presented in the texts were assessed by multiple-choice questions. 

More information is found in the following README'S:
* [preprocessing](./preprocessing_scripts/README.md)
* [participants](./participants/README.md)
* [stimuli](./stimuli/README.md)
* [eye-tracking data](./eyetracking_data/README.md)
* [additional processing](./additional_scripts/README.md)



## Data Overview
The data that was used to create the corpus and that was obtained during the experiments is made available in various stages. 
The data is stored in respective sub folders each of which contains a README that provides more information 
about the data and how to use it. **For a detailed description of the data types, format and content, please refer to the 
[CODEBOOK](./CODEBOOK.md).**

This repository contains the following data:
* **Eye-tracking data**
  * raw eye-tracking data
  * preprocessed eye-tracking data
* **Stimulus texts**
* **Anonymized participant data**
* **Scripts (in Python)**
  * scripts to preprocess the data
  * additional scripts that can be used to process the data further

The scripts were run using Python 3.9 with the dependencies specified in the `requirements.txt` file.


## Stimuli Annotation
The stimuli have been manually annoted with part-of-speech tags and other linguistic information. The annotations are described
in a separate file: [ANNOTATION](stimuli/ANNOTATION.md).

## Repository Structure
(to be deleted: to recreate structure adapt gitignore temporarily and do this:  tree --gitignore --filelimit 25 | tr '\240\240' ' ' > structure.txt)

    PoTeC-data
    ├── CODEBOOK.md
    ├── README.md
    ├── requirements.txt
    ├── additional_scripts
    │   ├── README.md
    │   ├── compute_reading_measures.py
    │   ├── errors
    │   │   └── merge_fixations_word_char_errors.txt
    │   ├── generate_scanpaths.py
    │   ├── merge_rm_wf.py
    │   └── merge_scanpaths_rm_wf.py
    ├── eyetracking_data
    │   ├── README.md
    │   ├── fixations
    │   ├── original_uncorrected_fixation_report.txt
    │   ├── raw_data 
    │   ├── reader_rm_wf
    │   ├── reading_measures
    │   ├── scanpaths
    │   └── scanpaths_reader_rm_wf
    ├── participants
    │   ├── README.md
    │   └── participant_data.tsv
    ├── preprocessing_scripts
    │   ├── README.md
    │   ├── char_index_to_word_index.py
    │   ├── create_word_roi_limits.py
    │   ├── roi_to_word.tsv
    │   ├── sent_limits.json
    │   └── word_limits.json
    └── stimuli
        ├── ANNOTATION.md
        ├── README.md
        ├── aoi_texts
        │   ├── b0.ias
        │   ├── b1.ias
        │   ├── b2.ias
        │   ├── b3.ias
        │   ├── b4.ias
        │   ├── b5.ias
        │   ├── p0.ias
        │   ├── p1.ias
        │   ├── p2.ias
        │   ├── p3.ias
        │   ├── p4.ias
        │   └── p5.ias
        ├── practice_items.txt
        ├── stimuli
        │   ├── bio_texts
        │   │   ├── b0.txt
        │   │   ├── b1.txt
        │   │   ├── b2.txt
        │   │   ├── b3.txt
        │   │   ├── b4.txt
        │   │   └── b5.txt
        │   ├── items.tsv
        │   ├── physics_texts
        │   │   ├── p0.txt
        │   │   ├── p1.txt
        │   │   ├── p2.txt
        │   │   ├── p3.txt
        │   │   ├── p4.txt
        │   │   └── p5.txt
        │   └── stimuli.tsv
        ├── stimuli.bib
        └── word_features
            ├── word_features_b0.tsv
            ├── word_features_b1.tsv
            ├── word_features_b2.tsv
            ├── word_features_b3.tsv
            ├── word_features_b4.tsv
            ├── word_features_b5.tsv
            ├── word_features_p0.tsv
            ├── word_features_p1.tsv
            ├── word_features_p2.tsv
            ├── word_features_p3.tsv
            ├── word_features_p4.tsv
            └── word_features_p5.tsv
