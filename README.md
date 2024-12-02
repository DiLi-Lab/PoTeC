# PoTeC - Potsdam Textbook Corpus

> :star2: :star2: If you'd like to ask a question, notice a mistake or want to say anything regarding the data please use the Discussions tab on GitHub. We're happy to hear your ideas and feeback!

This repository contains the Potsdam Textbook Corpus (PoTeC) which is a natural reading eye-tracking corpus.
Four groups of participants (expert/beginner level students of physics and biology) read 12 short 
texts taken from textbooks of physics and biology while their eye movements were monitored. 
The final dataset contains the reading data for 75 participants each reading all 12 texts.
The study follows a 2x2x2 fully-crossed factorial design:
* _Factor 1_: Study discipline of participant with the levels either physics or biology
* _Factor 2_: Study level of participant with the levels either beginner or expert
* _Factor 3_: Text domain with the levels either physics or biology

|              | Physics | Biology |
|--------------|---------|---------|
| **Beginner** | 12      | 16      |
| **Expert**   | 20      | 27      |

Both factors are quasi-experimental and manipulated between subjects.
The readers' text comprehension as well as their background
knowledge on the topics presented in the texts were assessed by multiple-choice questions.

More information is found in the following README'S:
* [preprocessing](./preprocessing_scripts/PREPROCESSING_SCRIPTS.md)
* [participants](./participants/README.md)
* [stimuli](./stimuli/STIMULI.md)
* [eye-tracking data](./eyetracking_data/EYETRACKING_DATA.md)
* [additional processing](./additional_scripts/ADDITIONAL_SCRIPTS.md)

**For a detailed description of the data types, format and content, please refer to the 
[CODEBOOK](./CODEBOOK.md).**

## Download the data
The data files are stored in an [OSF repository](https://osf.io/dn5hp/?view_only=). If this GitHub repository has been cloned, 
they can be downloaded and extracted automatically using the following script:

```bash
# or python3
python download_data_files.py

# OR to extract the files directly
python download_data_files.py --extract
```

Alternatively, they can be downloaded manually from the OSF repository and extracted into the respective folders.

## `pymovements` integration
PoTeC is integrated into the [pymovements](https://pymovements.readthedocs.io/en/stable/index.html) package. The package allows
to easily download the raw data and further process it. The following code snippet shows how to download the data:

```python
# pip install pymovements
import pymovements as pm

dataset = pm.Dataset('PoTeC', path='data/PoTeC')

dataset.download()
```

## Note on reading the data files using `pandas`
The German text p3 includes the word "null". If e.g. the word features are read using pandas, the word "null" is 
interpreted as a NA value. In order to avoid this behavior the command can be used with the following arguments:

```python
import pandas as pd
pd.read_csv('word_features_p3.tsv', sep='\t',  
            keep_default_na=False,
            na_values=['#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan',
                       '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NA', 'NaN', 'None', 'n/a',
                       'nan', '']
            )
```

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

|                           | **Setting**                                              | **Value**                                                                             |
|---------------------------|----------------------------------------------------------|---------------------------------------------------------------------------------------|
|                           |                                                          |                                                                                       |
| **Technical set-up**      | Eye-tracking device                                      | Eyelink 1000, dektop mounted camera system with a 35 mm lens                          |
|                           | Sampling rate                                            | 1000 Hz                                                                               |
|                           | Monitor size                                             | 47.5x30 cm, 22 inch                                                                   |
|                           | Monitor resolution                                       | 1680x1050 pixels                                                                      |
|                           | Eye-to-screen distance                                   | 61 cm                                                                                 |
|                           | Eye-to-camera distance                                   | 65 cm                                                                                 |
|                           | Experiment software                                      | Experiment Builder software provided by SR Research                                   |
|                           |                                                          |                                                                                       |
| **Stimulus presentation** | Background color                                         | Black                                                                                 |
|                           | Font color                                               | White                                                                                 |
|                           | Font size                                                | 18                                                                                    |
|                           | Font                                                     | Courier                                                                               |
|                           | Stimulus size                                            | On average 158 words shown on multiple lines on one page                              |
|                           | Number of characters per visual angle (middle of screen) | 2.8 characters per degree of visual angle                                             | 
|                           | Spacing                                                  |                                                                                       |

## Stimuli
The stimuli texts are made available via this [website](https://www.cl.uzh.ch/en/research-groups/digital-linguistics/resources/potec.html).

## Stimuli Annotation
The stimuli have been manually annoted with part-of-speech tags and other linguistic information. The annotations are described
in a separate file: [ANNOTATION](stimuli/ANNOTATION.md).

## Citation
```
@misc{potec,
    url={\url{https://github.com/DiLi-Lab/PoTeC}},
    author={Jakobi, Deborah N. and Kern, Thomas and Reich, David R. and Haller, Patrick and J\"ager, Lena A.},
    title={{PoTeC}: A {German} Naturalistic Eye-tracking-while-reading Corpus},
    year={2024},
    note={under review}
}
```


## Repository Structure

    PoTeC-data
    ├── CODEBOOK.md
    ├── README.md
    ├── requirements.txt
    ├── additional_scripts
    │   ├── ADDITIONAL_SCRIPTS.md
    │   ├── compute_reading_measures.py
    │   ├── generate_scanpaths.py
    │   ├── merge_reading_measures.py
    │   ├── create_codebook_tables.py
    │   ├── surprisal.py
    │   ├── get_surprisal.py
    │   ├── merge_fixations_and_coordinates.py
    │   ├── merge_scanpaths.py
    │   ├── analyses.R
    │   ├── run_bayesian_models.R
    │   ├── run_freq_models.R
    │   ├── all_colls_description.csv
    │   └── all_codebook_texts.csv
    ├── eyetracking_data
    │   ├── EYETRACKING_DATA.md
    │   ├── original_uncorrected_fixation_report.txt
    │   ├── fixations
    │   │   └── ...
    │   ├── fixations_uncorrected
    │   │   └── ...
    │   ├── asc_files
    │   │   └── ...
    │   ├── raw_data 
    │   │   └── ...
    │   ├── reader_merged
    │   │   └── ...
    │   ├── reading_measures
    │   │   └── ...
    │   ├── scanpaths
    │   │   └── ...
    │   └── scanpaths_merged
    │       └── ...
    ├── participants
    │   ├── PARTICIPANTS.md
    │   └── participant_data.tsv
    ├── preprocessing_scripts
    │   ├── PREPROCESSING_SCRIPTS.md
    │   ├── char_index_to_word_index.py
    │   ├── create_word_aoi_limits.py
    │   ├── correct_fixations.py
    │   ├── split_fixation_report.py
    │   ├── asc_to_csv.py
    │   ├── aoi_to_word.tsv
    │   ├── sent_limits.json
    │   └── word_limits.json
    └── stimuli
        ├── ANNOTATION.md
        ├── STIMULI.md
        ├── practice_items.txt
        ├── dependency_trees_manually_corrected.tsv
        ├── aoi_texts
        │   └── ...
        ├── stimuli
            ├── stimuli.bib
        │   ├── items.tsv
        │   └── stimuli.tsv
        └── word_features
            └── ...

