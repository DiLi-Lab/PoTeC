# Participants

**75 students** of the University of Potsdam all of whom were native speakers of German with normal or 
corrected-to-normal vision participated in the experiment. Participants with soft lenses were excluded 
from participation as soft lenses often pose serious challenges for the calibration of the eye-tracker.
They were **either students of biology or of physics** in either their **first semester of the BSc program (undergraduate) or graduate students currently attending a MSc or PhD program (graduate)**. Participants were 
requested to not  have consumed any alcohol the day of the experiment and  to not be suffering from sleep deprivation.
Participants received a minium compensation of 10 EUR and up to 20 EUR if they answered a specific number of comprehension 
questions correctly.

|              | Physics | Biology |
|--------------|---------|---------|
| **undergraduate** | 12      | 16      |
| **Advanced** | 20      | 27      |

## Demographic data
The field of studies (including  area specialization if applicable), the current semester of studies, gender, age, 
handedness, whether the participant was wearing contact lenses or glasses, hours of sleep the night before the 
experiment, alcohol consumption within 24h hours  before the experiment, whether or not the participant had grown 
up bilingually, and the state (Bundesland) where the German language was acquired were recorded. Some of that data is 
made available in the `participant_data.tsv` file. Please see the `CODEBOOK.md` for more information on the available information.


|      column  | description | value | range/choices | 
|--------------|---------|---------|---|
| **reader_id** | unique reader identifier     | int     | 0-105     |
| **reader_discipline** | reader's field of study     | categorical     |{pyhsics,biology}     |
| **reader_discipline_numeric** | numeric value of reader domain     | int   |  biology==0 physics==1    |
| **level_of_studies** | reader's level of studies    | categorical |{undergraduate, graduate}|
| **level_of_studies_numeric** | numerical value of level_of_studies     | int     |undergraduate==0 graduate==1     |
| **discipline_level_of_studies** | reader's domain expertise     | categorical |biology-undergraduate biology-graduate physics-undergraduate physics-graduate|
| **discipline_level_of_studies_numeric** | numerical value of level_of_studies     | int     |biology-undergraduate==0 biology-graduate==1 physics-undergraduate==2 physics-graduate==3     |
| **glasses** | whether reader had glasses     | categorical     |{yes,no,nan}     |
| **age** | reader's age     | float     | 18-41, nan     |
| **handedness** | reader's handedness     | categorical     | {right,left}     |
| **hours_sleep** | reader's number of sleep night before     | float     | 0-11   |
| **alcohol** | whether reader consumed alcohol night before experiment     | categorical     | {yes, no, nan}     |
| **gender** | reader's gender     | categorical     |male,female,nan     |
| **gender_numeric** | numerical value of reader's gender   | int     | male==0 female==1     |

