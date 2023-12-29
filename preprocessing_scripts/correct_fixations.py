# Input: 
# roi-files in aoi/<textid>.ias (nur ein file pro Text, unabhaengig von Leser, weil Fragen irrelevant)
# Fixations (Fixation report created by DataViewer software) in <fixfile> mit mindestens den Spalten ['RECORDING_SESSION_LABEL','itemid','CURRENT_FIX_INDEX', 'CURRENT_FIX_X', 'CURRENT_FIX_Y', 'CURRENT_FIX_DURATION', 'CURRENR_FIX_INTEREST_AREA_INDEX']
# liste readerIds (hier hart kodiert unten)
# liste textIds (hier hart kodiert unten)
# in readerIds und Fixation report reader 0_1 umbennen in 0

####
# Right/Left: Naechste/vorherige Fixation auswaehlen
# Up/Down:    Fixation nach unten/oben verschieben
# q/w:        Fixation nach rechts/links verschieben
# d/u:        Fixation loeschen (roi=-1) / wieder auf x,y->roi setzen
#
# alle fixs werden auf eine roi gemappt (auch diejenigen, die original auf keiner roi sind) oder muessen geloescht werden. geloeschte fixs werden nicht gespeichert und die restlichen gereindext (1 .. N)
#
# AusgabeDatei wird beim Fenster schließen erzeugt
#
# Wenn Ausgabedatei vorhanden, wird Trial uebersprungen (also loeschen, falls neu gemacht werde soll oder falls nicht richtig abgeschlossen wurde)
#
# in input daten in der zeichenspalte darf kein " oder ' sein (sed "s/[\"']/\*/g")
#
# scale=1, bis gefixt (s. todo)
#
# weil fixations geloescht und gereindext werden koennen, muessen in den ergebnissdateien ALLE spalten drin sein!

def makebg(roifile):
    with open(roifile) as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in csvreader:
            # print(row[6])
            if row[0][0] == '0':  # Nur Text (und nicht Fragen-) ROIs
                bg.create_rectangle(
                    (int(row[2]) // scale, int(row[3]) // scale, int(row[4]) // scale, int(row[5]) // scale),
                    tags=('roi', 'rectangle'), outline='slate gray', state='disabled')
                bg.create_text((((int(row[2]) + int(row[4])) / 2) // scale, ((int(row[3]) + int(row[5])) / 2) // scale),
                               text=row[6], tags=('roi', 'text'), fill='slate gray', state='disabled')


##erwartet 1.untere, 1.obere=2.unteregrenze, 2.obere=3.unteregrenze, ...
def fix2row(y, rowlimits):
    if rowlimits == []: return -1
    if y < rowlimits[0]: return -1
    return fix2row(y, rowlimits[1:]) + 1


# ROIs auslesen+malen (1.untere, 1.obere=2.untere, ...)
def getlimits(roifile):
    rowlimits = set()
    tmplimits = set()
    #  os.system('sed "s/[\"\']/*/g" '+roifile+' >> '+roifile) #replace quotes with * inplace
    with open(roifile, encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        i = 0
        for row in csvreader:
            i = i + 1
            if row[0][0] == '0':
                rowlimits.add(int(row[3]))  ##untere grenze ist nicht 0.
                rowlimits.add(int(row[5]))  ##untere grenze ist nicht 0.
                tmplimits.add((int(row[5]), int(row[2]), int(row[4])))
    rowlimits = sorted(rowlimits)
    collimits = [set() for _ in range(len(rowlimits) - 1)]
    for x in tmplimits:
        collimits[rowlimits.index(x[0]) - 1].add(x[1])
        collimits[rowlimits.index(x[0]) - 1].add(x[2])
    collimits = [sorted(x) for x in collimits]
    return rowlimits, collimits


# Generator to iterate over Fixationfiles
def readFixs(fixfile, readerIds, textIds):
    global roifile, title
    Fixations = pd.read_csv(fixfile, sep='\t', header='infer',
                            index_col=['RECORDING_SESSION_LABEL', 'itemid', 'CURRENT_FIX_INDEX'], )
    for reader in readerIds:
        for text in textIds:
            roifile = '/Users/debor/repos/PoTeC-data/stimuli/aoi_texts/' + text + '.ias'
            title = str(reader) + ' ' + text
            yield Fixations.loc[reader, text, :].sort_index()


# Focus fixation
def focus(index):
    bg.coords(focusobj, bg.coords(Fixs.loc[index, 'objid']))
    bg.tag_raise(focusobj)
    bg.tag_raise(Fixs.loc[fix_index, 'objid'])
    bg.tag_raise(Fixs.loc[fix_index, 'objid'] + 1)
    bg.tag_raise(Fixs.loc[fix_index, 'objid'] + 2)
    bg.tag_raise(Fixs.loc[fix_index, 'objid'] + 3)
    bg.tag_raise(Fixs.loc[fix_index, 'objid'] + 4)


def add(index):
    selected.append(index)
    bg.itemconfig(Fixs.loc[index, 'objid'], state='normal')


def roiindex(x, y):
    for i in range(y): x = x + len(collimits[i]) - 1  # -1, weil die collimits[i][0] die erste untere grenze ist...
    return x + 1  # +1, weil cols bei 0 anfaengt und roiindex bei 1


# Tastaturbindings
def keybindings(event):
    global fix_index
    #  print(event.keysym)
    if event.keysym == 'Right':
        if fix_index < Fixs.shape[0]:
            if fix_index > 0:
                bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 2, state='hidden')
                bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 3, state='hidden')
                bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 4, state='hidden')
            fix_index = fix_index + 1
            bg.itemconfig(Fixs.loc[fix_index, 'objid'], state='normal')
            bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 1, state='normal')
            bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 2, state='normal')
            bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 3, state='normal')
            bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 4, state='normal')
            focus(fix_index)
    elif event.keysym == 'Left':
        if fix_index > 0:
            bg.itemconfig(Fixs.loc[fix_index, 'objid'], state='disabled')
            bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 1, state='disabled')
            bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 2, state='hidden')
            bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 3, state='hidden')
            bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 4, state='hidden')
            fix_index = fix_index - 1
            if fix_index > 0:
                bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 2, state='normal')
                bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 3, state='normal')
                bg.itemconfig(Fixs.loc[fix_index, 'objid'] + 4, state='normal')
            focus(fix_index)
    elif event.keysym == 'Up':
        row = Fixs.loc[fix_index, 'line']
        col = Fixs.loc[fix_index, 'index_inline']
        fixindex = Fixs.loc[fix_index, 'roi']
        row = max(0, row - 1)
        col = max(0, fix2row(Fixs.loc[fix_index, 'CURRENT_FIX_X'], collimits[row]))  # Falls links vom ersten -> -1
        fixindex = roiindex(col, row)
        Fixs.set_value(fix_index, 'roi', fixindex)
        Fixs.set_value(fix_index, 'line', row)
        Fixs.set_value(fix_index, 'index_inline', col)
        rowl = rowlimits;
        coll = collimits[row]
        roix = (coll[col] + coll[col + 1]) / 2.
        roiy = (rowl[row] + rowl[row + 1]) / 2.
        bg.coords(Fixs.loc[fix_index, 'objid'] + 2, (
        roix // scale, roiy // scale, Fixs.loc[fix_index, 'CURRENT_FIX_X'] // scale,
        Fixs.loc[fix_index, 'CURRENT_FIX_Y'] // scale))
        bg.coords(Fixs.loc[fix_index, 'objid'] + 3,
                  ((roix - 4) // scale, (roiy - 4) // scale, (roix + 4) // scale, (roiy + 4) // scale))
        bg.coords(Fixs.loc[fix_index, 'objid'] + 4,
                  ((roix - 4) // scale, (roiy + 4) // scale, (roix + 4) // scale, (roiy - 4) // scale))
    elif event.keysym == 'Down':
        row = Fixs.loc[fix_index, 'line']
        col = Fixs.loc[fix_index, 'index_inline']
        fixindex = Fixs.loc[fix_index, 'roi']
        row = min(len(collimits), row + 1)  # Maximal letztes -> row+1
        col = max(0, fix2row(Fixs.loc[fix_index, 'CURRENT_FIX_X'], collimits[row]))  # Falls links vom ersten -> -1
        fixindex = roiindex(col, row)
        Fixs.set_value(fix_index, 'roi', fixindex)
        Fixs.set_value(fix_index, 'line', row)
        Fixs.set_value(fix_index, 'index_inline', col)
        rowl = rowlimits;
        coll = collimits[row]
        roix = (coll[col] + coll[col + 1]) / 2.
        roiy = (rowl[row] + rowl[row + 1]) / 2.
        bg.coords(Fixs.loc[fix_index, 'objid'] + 2, (
        roix // scale, roiy // scale, Fixs.loc[fix_index, 'CURRENT_FIX_X'] // scale,
        Fixs.loc[fix_index, 'CURRENT_FIX_Y'] // scale))
        bg.coords(Fixs.loc[fix_index, 'objid'] + 3,
                  ((roix - 4) // scale, (roiy - 4) // scale, (roix + 4) // scale, (roiy + 4) // scale))
        bg.coords(Fixs.loc[fix_index, 'objid'] + 4,
                  ((roix - 4) // scale, (roiy + 4) // scale, (roix + 4) // scale, (roiy - 4) // scale))
    elif event.keysym == 'q':
        row = Fixs.loc[fix_index, 'line']
        col = Fixs.loc[fix_index, 'index_inline']
        fixindex = Fixs.loc[fix_index, 'roi']

        col = max(0, col - 1)
        fixindex = roiindex(col, row)
        Fixs.set_value(fix_index, 'roi', fixindex)
        Fixs.set_value(fix_index, 'line', row)
        Fixs.set_value(fix_index, 'index_inline', col)

        rowl = rowlimits;
        coll = collimits[row]
        roix = (coll[col] + coll[col + 1]) / 2.
        roiy = (rowl[row] + rowl[row + 1]) / 2.
        bg.coords(Fixs.loc[fix_index, 'objid'] + 2, (
        roix // scale, roiy // scale, Fixs.loc[fix_index, 'CURRENT_FIX_X'] // scale,
        Fixs.loc[fix_index, 'CURRENT_FIX_Y'] // scale))
        bg.coords(Fixs.loc[fix_index, 'objid'] + 3,
                  ((roix - 4) // scale, (roiy - 4) // scale, (roix + 4) // scale, (roiy + 4) // scale))
        bg.coords(Fixs.loc[fix_index, 'objid'] + 4,
                  ((roix - 4) // scale, (roiy + 4) // scale, (roix + 4) // scale, (roiy - 4) // scale))
    elif event.keysym == 'w':
        row = Fixs.loc[fix_index, 'line']
        col = Fixs.loc[fix_index, 'index_inline']
        fixindex = Fixs.loc[fix_index, 'roi']

        col = min(len(collimits[row]), col + 1)
        fixindex = roiindex(col, row)
        Fixs.set_value(fix_index, 'roi', fixindex)
        Fixs.set_value(fix_index, 'line', row)
        Fixs.set_value(fix_index, 'index_inline', col)

        rowl = rowlimits;
        coll = collimits[row]
        roix = (coll[col] + coll[col + 1]) / 2.
        roiy = (rowl[row] + rowl[row + 1]) / 2.
        bg.coords(Fixs.loc[fix_index, 'objid'] + 2, (
        roix // scale, roiy // scale, Fixs.loc[fix_index, 'CURRENT_FIX_X'] // scale,
        Fixs.loc[fix_index, 'CURRENT_FIX_Y'] // scale))
        bg.coords(Fixs.loc[fix_index, 'objid'] + 3,
                  ((roix - 4) // scale, (roiy - 4) // scale, (roix + 4) // scale, (roiy + 4) // scale))
        bg.coords(Fixs.loc[fix_index, 'objid'] + 4,
                  ((roix - 4) // scale, (roiy + 4) // scale, (roix + 4) // scale, (roiy - 4) // scale))
    elif event.keysym == 'd':  # delete
        Fixs.set_value(fix_index, 'roi', -1)
        bg.itemconfig(Fixs.loc[fix_index, 'objid'], outline='red')
        bg.itemconfig(Fixs.loc[fix_index, 'objid'], disabledoutline='red')
    elif event.keysym == 'u':  # undelete
        x = Fixs.loc[fix_index, 'CURRENT_FIX_X'];
        y = Fixs.loc[fix_index, 'CURRENT_FIX_Y'];
        row = fix2row(y, rowlimits)
        row = max(row, 0)
        row = min(row, len(collimits) - 1)
        col = fix2row(x, collimits[row])
        col = max(col, 0)
        col = min(col, len(collimits[row]) - 2)
        rowl = rowlimits;
        coll = collimits[row]
        # print(col,len(coll))
        roix = (coll[col] + coll[col + 1]) / 2.
        roiy = (rowl[row] + rowl[row + 1]) / 2.

        Fixs.set_value(fix_index, 'roi', roiindex(col, row))
        Fixs.set_value(fix_index, 'line', row)
        Fixs.set_value(fix_index, 'index_inline', col)
        bg.itemconfig(Fixs.loc[fix_index, 'objid'], outline='white')
        bg.itemconfig(Fixs.loc[fix_index, 'objid'], disabledoutline='slate gray')


#  elif event.keysym=='Return':
#    w.itemconfig(Fixs.loc[fix_index],state='disabled')
#  elif event.keysym=='space':
#    add(fix_index)
#  print(bg.coords(Fixs.loc[fix_index,'objid']))


import tkinter as tk  # malen
import pandas as pd  # csv lesesn
import numpy as np
import os
import csv
import collections  # namedtuples

# import operator

scale = 1.4  # windowscaling (alles geteilt durch scale)
roifile = ''
reader = ''
fixfile = '/Users/debor/repos/PoTeC-data/eyetracking_data/original_uncorrected_fixation_report.txt'
readerIds = [71, 18, 67, 20, 3, 9, 12, 13, 10, 23, 8, 69, 96, 98, 62, 84, 5, 94, 102, 95, 104, 97, 37, 34, 17, 66, 90,
             39, 2, 31, 30, 14, 15, 19, 77, 92, 85, 68, 99, 105, 36, 65, 87, 100, 0, 73, 64, 72, 91, 38, 76, 40, 4, 79,
             80, 101, 16, 63, 74, 6, 70, 35, 93, 7, 83, 1, 82, 78, 32, 61, 75, 81, 60, 103, 41, 22]

textIds = ['b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'p0', 'p1', 'p2', 'p3', 'p4', 'p5']

# Fixations nach reader, text, index durchgehen:
for Fixs in readFixs(fixfile, readerIds, textIds):  # generator erzeugen, savebutton next() binden
    if os.path.isfile('reader' + title[:-3] + '_' + roifile[-6:-4] + '.justfix'): continue
    # Ausgabefenster
    window = tk.Tk()
    window.title(title)
    bg = tk.Canvas(window, width=1680 // scale, height=1050 // scale, background='black')
    bg.bind('<KeyPress>', keybindings)
    bg.pack()
    bg.focus_set()

    # ROIs lesen und malen
    rowlimits, collimits = getlimits(roifile)
    makebg(roifile)
    for rowindex, row in enumerate(rowlimits):
        bg.create_line(
            ((collimits[rowindex - 1][0]) // scale, row // scale, (collimits[rowindex - 1][-1]) // scale, row // scale),
            fill='red')

    old_x = 0;
    old_y = 0;
    fix_index = 0
    focusobj = bg.create_oval(0, 0, 0, 0, tags=('focus'), fill='green', width=1.7)
    objid = [];
    roi = [];
    line = [];
    index_inline = [];
    roiend = []
    for fix in Fixs.itertuples():
        x = fix.CURRENT_FIX_X;
        y = fix.CURRENT_FIX_Y;
        r = (fix.CURRENT_FIX_DURATION / 20)
        row = fix2row(y, rowlimits)
        row = max(row, 0)
        row = min(row, len(collimits) - 1)
        col = fix2row(x, collimits[row])
        col = max(col, 0)
        col = min(col, len(collimits[row]) - 2)
        rowl = rowlimits;
        coll = collimits[row]
        # print(col,len(coll))
        roix = (coll[col] + coll[col + 1]) / 2.
        roiy = (rowl[row] + rowl[row + 1]) / 2.
        roi.append(roiindex(col, row))
        line.append(row)
        index_inline.append(col)
        objid.append(bg.create_oval(((x - r) // scale, (y - r) // scale, (x + r) // scale, (y + r) // scale),
                                    tags=('fix', 'line', 'a' + str(fix.Index)), state='disabled', outline='white',
                                    disabledoutline='slate gray', width=1.7))
        bg.create_line((old_x // scale, old_y // scale, x // scale, y // scale),
                       tags=('fix', 'line', 'a' + str(fix.Index)), state='disabled', fill='white',
                       disabledfill='slate gray')
        bg.create_line((roix // scale, roiy // scale, x // scale, y // scale),
                       tags=('fix', 'line', 'a' + str(fix.Index)), state='hidden', fill='white',
                       disabledfill='slate gray', width=4)
        bg.create_line(((roix - 4) // scale, (roiy - 4) // scale, (roix + 4) // scale, (roiy + 4) // scale),
                       tags=('fix', 'line', 'a' + str(fix.Index)), state='hidden', fill='white',
                       disabledfill='slate gray', width=4)
        bg.create_line(((roix - 4) // scale, (roiy + 4) // scale, (roix + 4) // scale, (roiy - 4) // scale),
                       tags=('fix', 'line', 'a' + str(fix.Index)), state='hidden', fill='white',
                       disabledfill='slate gray', width=4)
        old_x = x;
        old_y = y
    Fixs['objid'] = objid
    Fixs['line'] = line
    Fixs['roi'] = roi
    Fixs['index_inline'] = index_inline

    selected = []
    # Einruecken fuer for-loop..
    window.mainloop()
    # print(Fixs)
    #  Fixs['roiend']=[Fixs['roi']-[]Fixs['roi']]
    Fixs.to_csv(path_or_buf='blub.tst', sep='\t', na_rep='.', float_format=None, columns=None, header=True, index=True,
                index_label=None, mode='w', encoding=None, compression=None, quoting=None, quotechar='"',
                line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True,
                escapechar=None, decimal='.')  # TODO: scale bringt roimappings durcheinander, scale=1 bis gefixt
    Fixs['line'] = Fixs['line'] + 1  # damits konsistent bei 1 losgeht
    Fixs['index_inline'] = Fixs['index_inline'] + 1
    NFix = Fixs.shape[0]
    Fixs = Fixs[Fixs['roi'] > 0]  # als geloescht markierte (-1) fuer ausgabe loeschen
    Fixs[
        'ORIGINAL_CURRENT_FIX_INDEX'] = Fixs.index  # alten CURRENT_FIX_INDEX speichern um bei Bedarf mit Originaldaten mappen zu kennen
    Fixs.index = [i + 1 for i in range(Fixs.shape[0])]  # reindex
    os.system('echo "Number of deleted Fixations in "' + title + ': ' + str(NFix - Fixs.shape[0]) + ' >> trimFix.log')
    Fixs['Fix_adjusted'] = Fixs['roi'].astype(str) != Fixs['CURRENT_FIX_INTEREST_AREA_INDEX']
    os.system('echo "Number of adjusted Fixations in "' + title + ': ' + str(
        np.sum(Fixs['Fix_adjusted'])) + ' >> trimFix.log')
    Fixs['RECORDING_SESSION_LABEL'] = title[:-3]
    Fixs['itemid'] = roifile[-6:-4]
    Fixs = Fixs.drop(['CURRENT_FIX_INTEREST_AREA_INDEX', 'CURRENT_FIX_X', 'CURRENT_FIX_Y', 'objid'], axis=1)
    Fixs.to_csv(path_or_buf='reader' + title[:-3] + '_' + roifile[-6:-4] + '.justfix', sep='\t', na_rep='.',
                float_format=None, header=True, index=True, index_label='CURRENT_FIX_INDEX', mode='w', encoding=None,
                compression=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None,
                tupleize_cols=False, date_format=None, doublequote=True, escapechar=None, decimal='.')
