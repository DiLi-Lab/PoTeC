#!/usr/bin/env python3
"""
#TODO
Call: #TODO
"""

# TODO: FIX
import re
import os

# files = [f for f in os.listdir('../data') if re.match(r'.*.asc', f)] 32.asc und 62.asc sind kaputt TODO loeschen
#  files = ['63.asc', '64.asc', '65.asc', '66.asc', '67.asc', '68.asc', '69.asc', '7.asc', '70.asc', '71.asc',
#  '72.asc', '73.asc', '74.asc', '75.asc', '76.asc', '77.asc', '78.asc', '79.asc', '8.asc', '80.asc', '81.asc',
#  '82.asc', '83.asc', '84.asc', '85.asc', '87.asc', '9.asc', '90.asc', '91.asc', '92.asc', '93.asc', '94.asc',
#  '95.asc', '96.asc', '97.asc', '98.asc', '99.asc']

files = ['62.asc']
# files = ['32.asc'] files = ['31.asc', '32.asc', '34.asc', '35.asc', '36.asc', '37.asc', '38.asc', '39.asc',
# '4.asc', '40.asc', '41.asc', '5.asc', '6.asc', '60.asc', '61.asc', '62.asc', '63.asc', '64.asc', '65.asc',
# '66.asc', '67.asc', '68.asc', '69.asc', '7.asc', '70.asc', '71.asc', '72.asc', '73.asc', '74.asc', '75.asc',
# '76.asc', '77.asc', '78.asc', '79.asc', '8.asc', '80.asc', '81.asc', '82.asc', '83.asc', '84.asc', '85.asc',
# '87.asc', '9.asc', '90.asc', '91.asc', '92.asc', '93.asc', '94.asc', '95.asc', '96.asc', '97.asc', '98.asc', '99.asc']


on = re.compile('.*SYNCTIME\.sentence')  # todo matcht hier auch SYNCTIME.sentence_Practice?
off = re.compile('.*sentence\.STOP')
tr = re.compile('.*TRIAL_VAR trial (.*)')  # line containing trial id
tx = re.compile('.*TRIAL_VAR itemid (.*)')  # # line containing text id
sample = re.compile('[0-9].*')  # any line starting with a number is a sample
practice_on = re.compile(
    '.*SYNCTIME_sentence_Practice')  # if practice trial (fix for files where practice was recorded)
practice_off = re.compile('.*TRIALID 1')  # in files with practice data, TRIALID 1 marks end of practice (but not in
# other files!


for file in files:
    with open(os.path.join('../data', file), 'r') as f:
        id = file.split('.')[0]  # reader id
        select = False
        practice = False
        practice_done = False
        trial = None
        text = None

        for line in f.readlines():

            if not practice_done:  # skip practice trial recording
                if practice_on.match(line):
                    practice = True
                    continue

            if select:  # if parsing eye mov samples
                if off.match(line):  # end of eye movements on text
                    select = False
                    continue

                elif sample.match(line):  # if line is a sample (not a message)
                    with open('temp', 'a') as f_out:
                        f_out.write(line)
                        continue

            elif on.match(line):  # begin of eye movements on text
                select = True
                trial = None  # in sessions with practice recordings, trial and item are set many times at unpredictable times
                text = None
                practice = False  # in sessions where practice is recorded, now done
                practice_done = True
                # write header
                with open('temp', 'w') as f_out:
                    f_out.write('time\t x\t y\t pupil_diameter\t other\t dots\n')
                    continue

            elif not select and not practice:
                # look for trial and text id only outside of eye mov samples and
                # outside practice
                # get trial id
                if tr.match(line):  # if line contains trial id
                    m = tr.match(line)
                    trial = m.group(1)  # (erste) Klammer in regex enthaelt trial id
                    continue

                # get text id
                elif tx.match(line):  # if line contains text id
                    n = tx.match(line)  # match
                    text = n.group(1)  # (erste) Klammer in regex enthaelt text id
                    continue

            if trial and text:
                try:
                    # in sessions with practice, all trial DVs (including trial and item) were send 12 times rather
                    # than once; in these cases, temp does not exist after the first encounter; therefore skip all
                    # except for the first occurrence
                    os.rename('temp', id + '_' + text + '_trial' + trial + '.csv')
                    trial = None
                    text = None

                except FileNotFoundError:  # temp has not been created
                    trial = None  # here, trial, text must have been set before the next eye mov section was parsed (
                    # in files with practice trial recodrding, variables are written multiple times to data)
                    text = None
    print(file)
