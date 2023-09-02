# Reading Measures

Continuous Measures

| Measure                            | Abbreviation | Definition                                                                                                                                                                                                                                                 |
|------------------------------------|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| first-fixation duration            | FFD          | duration of the first fixation on a word if this word is fixated in first-pass reading, otherwise 0                                                                                                                                                        |
| first duration                     | FD           | duration of the first fixation on a word (identical to FFD if not skipped in the first-pass)                                                                                                                                                               |
| first-pass reading time            | FPRT         | sum of the durations of all first-pass fixations on a word (0 if the word was skipped in the first-pass)                                                                                                                                                   |
| single-fixation duration           | SFD          | duration of the only first-pass fixation on a word, 0 if the word was skipped or more than one fixations occurred in the first-pass (equals FFD in case of a single first-pass fixation)                                                                   |
| first-reading time                 | FRT          | sum of the duration of all fixations from first fixating the word (independent if the first fixations occurs in first-pass reading) until leaving the word for the first time (equals FPRT in case the word was fixated in the first-pass)                 |
| total-fixation time                | TFT          | sum of all fixations on a word (FPRT+RRT)                                                                                                                                                                                                                  |
| re-reading time                    | RRT          | sum of the durations of all fixations on a word that do not belong to the first-pass (TFT-FPRT)                                                                                                                                                            |
| inclusive regression-path duration | RPD_inc      | sum of all fixation durations starting from the first first-pass fixation on a word until fixation a word to the right of this word (including all regressive fixations on previous words), 0 if the word was not fixated in the first-pass (RPD_exc+RBRT) |
| exclusive regression-path duration | RPD_exc      | sum of all fixation durations after initiating a first-pass regression from a word until fixating a word to the right of this word, without counting fixations on the word itself (RPD_inc-RBRT)                                                           |
| right-bounded reading time         | RBRT         | sum of all fixation durations on a word until a word to the right of this word is fixated (RPD_inc-RDP_exc)                                                                                                                                                |

Binary Measures

| Measure               | Abbreviation | Definition                                                                                         |
|-----------------------|--------------|----------------------------------------------------------------------------------------------------|
| fixation              | Fix          | 1 if the word was fixated, otherwise 0 (FPF or RR)                                                 |
| first-pass fixation   | FPF          | 1 if the word was fixated in the first-pass, otherwise 0                                           |
| first-pass regression | FPReg        | 1 if a regression was initiated in the first-pass reading of the word, otherwise 0 (sign(RPD exc)) |
| re-reading            | RR           | 1 if the word was fixated after the first-pass reading, otherwise 0 (sign(RRT))                    |

Ordinal Measures

| Measure                             | Abbreviation | Definition                                                                                                                                                                                  |
|-------------------------------------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| landing position                    | LP           | position of the first saccade on the word expressed by ordinal position of the fixated character                                                                                            |
| incoming saccade length             | SL_in        | length of the saccade that leads to first fixation on a word in number of words; positive sign if the saccade is a progressive one, negative sign if it is a regression                     |
| outgoing saccade length             | SL_out       | length of the first saccade that leaves the word in number of words; positive sign if the saccade is a progressive one, negative sign if it is a regression; 0 if the word is never fixated |
| total count of incoming regressions | TRC_out      | total number of regressive saccades initiated from this word                                                                                                                                |
| total count of outgoing regressions | TRC_in       | total number of regressive saccades landing on this word                                                                                                                                    |