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
* [preprocessing](./preprocessing_scripts/README.md).
* [participants](./participants/README.md)
* [stimuli](./stimuli/README.md)
* [eye-tracking data](./eyetracking_data/README.md)
* [additional processing](./additional_scripts/REAMDE.md)



## Data Overview
All the data that was used to create the corpus and that was obtained during the experiments is made available. 
The data is stored in respective sub folders each of which contains a README that provides more information 
about the data and how to use it. **For a detailed description of the data types, format and content, please refer to the 
[CODEBOOK](./CODEBOOK.md).**

This repository contains the following data:
* **Eye-tracking data**
  * raw eye-tracking data
  * preprocessed eye-tracking data
* **Stimulus texts**

--> ich habe Marie-Luise gefragt, sie hat mir das gesagt (Wir können uns auf 60c (1) 2. beziehen. Dann müssen wir allerdings das OSF repo vlt so machen, dass sie Leute sich einloggen müssen, um die Daten zu erhalten. Dann würde das vermutlich als 'einzelne Dritte' gelten.):
 https://www.gesetze-im-internet.de/urhg/BJNR012730965.html#BJNR012730965BJNG001302123
New
10:09
"§ 60c Wissenschaftliche Forschung
(1) Zum Zweck der nicht kommerziellen wissenschaftlichen Forschung dürfen bis zu 15 Prozent eines Werkes vervielfältigt, verbreitet und öffentlich zugänglich gemacht werden
1.
für einen bestimmt abgegrenzten Kreis von Personen für deren eigene wissenschaftliche Forschung sowie
2.
für einzelne Dritte, soweit dies der Überprüfung der Qualität wissenschaftlicher Forschung dient.
(2) Für die eigene wissenschaftliche Forschung dürfen bis zu 75 Prozent eines Werkes vervielfältigt werden.
(3) Abbildungen, einzelne Beiträge aus derselben Fachzeitschrift oder wissenschaftlichen Zeitschrift, sonstige Werke geringen Umfangs und vergriffene Werke dürfen abweichend von den Absätzen 1 und 2 vollständig genutzt werden.
(4) Nicht nach den Absätzen 1 bis 3 erlaubt ist es, während öffentlicher Vorträge, Aufführungen oder Vorführungen eines Werkes diese auf Bild- oder Tonträger aufzunehmen und später öffentlich zugänglich zu machen."

* **Anonymized participant data**
* **Scripts (in Python)**
  * scripts to preprocess the data
  * additional scripts that can be used to process the data further

The scripts were run using Python 3.9 with the dependencies specified in the `requirements.txt` file 
in the top folder.

----> Kannst du vielleicht auch noch eine Art Baum zeichnen, der darstellt, wie das preprocessing durchgeführt wird/wurde (also welches skript angewendet wird um dann welchen datensatz zu erzeugen)?




## Stimuli Annotation
The stimuli have been manually annoted with part-of-speech tags and other linguistic information. The annotations are described
in a separate file: [ANNOTATION](stimuli/ANNOTATION.md).

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
    ├── comprehension_questions
    ├── CODEBOOK.md
    └── README.md


