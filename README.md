# PoTeC - Potsdam Textbook Corpus

This repository contains Potsdam Textbook Corpus (PoTeC) which is a natural reading eye-tracking corpus.
Four groups of participants (expert/beginner level students of physics and biology) read 12 short 
texts taken from textbooks of physics and biology while their eye movements were monitored. 
The final dataset contains the reading data for 75 participants each reading all 12 texts.
The study follows a 2x2 fully-crossed factorial design:
* _Factor 1_: Study major with the levels either physics or biology
* _Factor 2_: Level of expertise with the levels either beginner or expert

|              | Physics | Biology |
|--------------|---------|---------|
| **Beginner** | 12      | 16      |
| **Expert**   | 20      | 27      |

Both factors are quasi-experimental and manipulated between subjects.
The readers' text comprehension as well as their background 
knowledge in the topics presented in the texts were assessed by multiple-choice questions. 

More information is found in the following README'S:
* [preprocessing](./preprocessing_scripts/PREPROCESSING_SCRIPTS.md)
* [participants](./participants/README.md)
* [stimuli](./stimuli/STIMULI.md)
* [eye-tracking data](./eyetracking_data/EYETRACKING_DATA.md)
* [additional processing](./additional_scripts/ADDITIONAL_SCRIPTS.md)



## Data Overview
The data that was used to create the corpus and that was obtained during the experiments is made available in various stages. 
The data is stored in respective sub folders each of which contains a README that provides more information 
about the data and how to use it. **For a detailed description of the data types, format and content, please refer to the 
[CODEBOOK](./CODEBOOK.md).**

This repository contains the following data:
* **Eye-tracking data**
  * raw eye-tracking data
  * preprocessed eye-tracking data
* **Stimuli**
  * stimuli texts
  * text and background questions
* **Anonymized participant data**
* **Scripts (in Python)**
  * scripts to preprocess the data
  * additional scripts that have been used to process the data further

The scripts were run using Python 3.9 with the dependencies specified in the `requirements.txt` file.

## Technical set-up
The experiment was run with the following technical set-up:

|                           | **Setting**            | **Value**                                                    |
|---------------------------|------------------------|--------------------------------------------------------------|
|                           |                        |                                                              |
| **Technical set-up**      | Eye-tracking device    | Eyelink 1000, dektop mounted camera system with a 35 mm lens |
|                           | Sampling rate          | 1000 Hz                                                      |
|                           | Monitor size           | 22 inch                                                      |
|                           | Monitor resolution     | 1680x1050 pixels                                             |
|                           | Eye-to-screen distance | 61 cm                                                        |
|                           | Eye-to-camera distance | 65 cm                                                        |
|                           | Experiment software    | Experiment Builder software provided by SR Research          |
|                           |                        |                                                              |
| **Stimulus presentation** | Background color       | Black                                                        |
|                           | Font color             | White                                                        |
|                           | Font size              | 18                                                           |
|                           | Font                   | Courier                                                      |
|                           | Stimulus size          | On average 158 words shown on multiple lines on one page     |
|                           |                        |                                                              |
|                           |                        |                                                              |

## Stimuli Annotation
The stimuli have been manually annoted with part-of-speech tags and other linguistic information. The annotations are described
in a separate file: [ANNOTATION](stimuli/ANNOTATION.md).

## Repository Structure

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
    │   ├── original_uncorrected_fixation_report.txt
    │   ├── fixations
    │   │   └── ...
    │   ├── raw_data 
    │   │   └── ...
    │   ├── reader_rm_wf
    │   │   └── ...
    │   ├── reading_measures
    │   │   └── ...
    │   ├── scanpaths
    │   │   └── ...
    │   └── scanpaths_reader_rm_wf
    │       └── ...
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
        ├── stimuli.bib
        ├── aoi_texts
        │   └── ...
        ├── practice_items.txt
        ├── stimuli
        │   ├── bio_texts
        │   │   └── ...
        │   ├── physics_texts
        │   │   └── ...
        │   ├── items.tsv
        │   └── stimuli.tsv
        └── word_features
            └── ...

