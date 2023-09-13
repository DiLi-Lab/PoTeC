We also need a participants section where we define the inclusion criteria 
(they are simple: beginner = 1st semester; advanced=graduate student pursuing a Master's or phd degree); 
students who were or had been studying both majors were excluded from participation; 
weitere kriterien: native speaker of German, normal or corrected-to-normal vision


|      column  | description | value | range/choices | 
|--------------|---------|---------|---|
| **reader_id** | unique reader identifier     | int     | 0-105     |
| **reader_domain** | reader's field of study     | categorical     |{pyhsics,biology}     |
| **reader_domain_numeric** | numeric value of reader domain     | int   |  biology==0 physics==1    |
| **expert_status** | reader's expert status    | categorical |{beginner, expert}|
| **expert_status_numeric** | numerical value of expert_status     | int     |beginner==0 expert==1     |
| **domain_expert_status** | reader's domain expertise     | categorical |biology-beginner biology-expert physics-beginner physics-expert|
| **domain_expert_status_numeric** | numerical value of expert_status     | int     |biology-beginner==0 biology-expert==1 physics-beginner==2 physics-expert==3     |
| **glasses** | whether reader had glasses     | categorical     |{yes,no,nan}     |
| **age** | reader's age     | float     | 18-41, nan     |
| **handedness** | reader's handedness     | categorical     | {right,left}     |
| **hours_sleep** | reader's number of sleep night before     | float     | 0-11   |
| **alcohol** | whether reader consumed alcohol night before experiment     | categorical     | {yes, no, nan}     |
| **gender** | reader's gender     | categorical     |male,female,nan     |
| **gender_numeric** | numerical value of reader's gender   | int     | male==0 female==1     |

