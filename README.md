# PoTeC - Potsdam Textbook Corpus

This repository contains eye-tracking data, the Potsdam Textbook Corpus (PoTeC). 
4 groups of participants (advanced/beginner level students of physics and biology) read a series of short 
texts taken from textbooks of physics and biology while their eye movements were monitored
(each participant reads all texts). Their text comprehension as well as their background 
knowledge in the topics presented in the texts were assessed by multiple-choice comprehension questions.
--> I would add a somewhat more formal description of the experimental design: 
Fully-crossed 2x2 factorial design. Both factors are quasi-experimental and manipulated between subjects. 
Factor 1: Study major with the levels={physics, biology}
Factor 2: Level of expertise with the levels={beginner; advanced}
--> Du kannst die Faktoren auch anders nennen; es sollte nur konsistent sein in readme, code/data und paper

We also need a participants section where we define the inclusion criteria (they are simple: beginner = 1st semester; advanced=graduate student pursuing a Master's or phd degree); students who were or had been studying both majors were excluded from participation; weitere kriterien: native speaker of German, normal or corrected-to-normal vision

## Data
All the data that was used to create the corpus and that was obtained during the experiments is made available. 
The data is stored in respective sub folders each of which contains a README that provides more information 
about the data and how to use it.

This repository contains the following data:
* **Eye-tracking data**
  * raw eye-tracking data
  * preprocessed eye-tracking data
* ~~**Stimulus texts**~~ --> we're not allowed right? --> I think we are allowed since it is only excerpts of less than 10%. We need to double check this (maybe ask Marie-Luise how to find this out, she did this for MultiplEYE).

  --> we also need to mention all the annotations that we provide (part-of-speech, and all the handcrafted tags, and the corpus-based features, and surprisal etc.). We should briefly describe them here.
  --> die Quelle der stimuli (Referenz mit seitenangabe) muss auch unbedingt rein.
  
* **Anonymized participant data**
* **Scripts (in Python)**
  * scripts to preprocess the data
  * additional scripts that can be used to process the data further

The scripts were run using Python 3.9 with the dependencies specified in the `requirements.txt` file 
in the top folder.

-----> We also need to provide some kind of code book where we define the column names of all data files. 
---> aus der repository structure hier unten geht nicht klar hervor, was welches der skripte tut. Das sollte auch noch irgendwo rein.

----> Kannst du vielleicht auch noch eine Art Baum zeichnen, der darstellt, wie das preprocessing durchgeführt wird/wurde (also welches skript angewendet wird um dann welchen datensatz zu erzeugen)?

Es wäre auch gut, wenn du das ganze mal Marie-Luise zeigen könntest und sie um Feedback fragen könntest. 

Und es fehlt auch noch Informationen zu den comprehension questions und wie sie kodiert sind. 


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


