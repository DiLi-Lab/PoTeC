# PoTeC - Potsdam Textbook Corpus

This repository contains eye-tracking data, the Potsdam Textbook Corpus (PoTeC). 
4 groups of participants (advanced/beginner level students of physics and biology) read a series of short 
texts taken from textbooks of physics and biology while their eye movements were monitored
(each participant reads all texts). Their text comprehension as well as their background 
knowledge in the topics presented in the texts were assessed by multiple-choice comprehension questions.

## Data
All the data that was used to create the corpus and that was obtained during the experiments in made available. 
The data is stored in respective sub folders each of which contains a README that provides more information 
about the data and how to use it.

This repository contains the following data:
* **Eye-tracking data**
  * raw eye-tracking data
  * preprocessed eye-tracking data
* ~~**Stimulus texts**~~ --> we're not allowed right?
* **Anonymized participant data**
* **Scripts (in Python)**
  * scripts to preprocess the data
  * additional scripts that can be used to process the data further

The scripts were run using Python 3.9 with the dependencies specified in the `requirements.txt` file 
in the top folder.

## Repository Structure
    PoTeC
    ├── eyetracking_data
    │ ├── fixations
    │ ├── raw_data
    │ └── ... [other folders depending on the additional scripts]
    ├── participants
    │ ├── participant_data.csv
    │ └── readerIDs.txt
    ├── additional_scripts
    │ ├── merge_fixations+word+char.py
    │ ├── merge_reading_measures+word_features.py
    │ └── merge_scanpaths+reader_information.py
    ├── preprocessing
    │ ├── ...
    │ ├── ...
    │ ├── ...
    │ ├── ...
    │ ├── ...
    │ ├── ...
    │ ├── ...
    │ └── ...
    ├──  stimuli
    │ ├── aoi_texts
    │ ├── text_tags
    │ ├── text_examples
    │ ├── texts
    │ └── word_features
    └── README.md


