# -*- coding: utf-8 -*-
#
#    bip39-dutch createlist.py
#    Copyright (C) 2016 October 
#    1200 Web Development
#    http://1200wd.com/
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

DICTFILE = 'wordlist/dutch.txt'
FREQFILE = 'wordlist/dutch-frequency.txt'
TYPEFILE = 'wordlist/dutch-type.txt'
BADWORDSFILE = 'wordlist/dutch-bad.txt'
FORBIDDEN_CHARS = [' ', '-', '.', ',']
OUTPUTFILE = 'wordlist/dutch-bip39.txt'
SIMILAR = (
    ('a', 'c'), ('a', 'e'), ('a', 'o'),
    ('b', 'd'), ('b', 'h'), ('b', 'p'), ('b', 'q'), ('b', 'r'),
    ('c', 'e'), ('c', 'g'), ('c', 'n'), ('c', 'o'), ('c', 'q'), ('c', 'u'),
    ('d', 'g'), ('d', 'h'), ('d', 'o'), ('d', 'p'), ('d', 'q'),
    ('e', 'f'), ('e', 'o'),
    ('f', 'i'), ('f', 'j'), ('f', 'l'), ('f', 'p'), ('f', 't'),
    ('g', 'j'), ('g', 'o'), ('g', 'p'), ('g', 'q'), ('g', 'y'),
    ('h', 'k'), ('h', 'l'), ('h', 'm'), ('h', 'n'), ('h', 'r'),
    ('i', 'j'), ('i', 'l'), ('i', 't'), ('i', 'y'),
    ('j', 'l'), ('j', 'p'), ('j', 'q'), ('j', 'y'),
    ('k', 'x'),
    ('l', 't'),
    ('m', 'n'), ('m', 'w'),
    ('n', 'u'), ('n', 'z'),
    ('o', 'p'), ('o', 'q'), ('o', 'u'), ('o', 'v'),
    ('p', 'q'), ('p', 'r'),
    ('q', 'y'),
    ('s', 'z'),
    ('u', 'v'), ('u', 'w'), ('u', 'y'),
    ('v', 'w'), ('v', 'y')
)


def frequency():
    wf = {}
    f = open(FREQFILE, 'r')
    for wl in f.readlines():
        line = wl.split('\t')
        try:
            wf.update({
                line[0]: int(line[1]) or 0,
            })
        except:
            pass
    return wf

def wordtypes():
    wt = {}
    f = open(TYPEFILE, 'r')
    for wl in f.readlines():
        line = wl.split('/')
        try:
            wt.update({
                line[0].lower(): line[1].replace('\n',''),
            })
        except:
            pass
    return wt

def similar_words(w1, w2):
    if len(w1) != len(w2):
        return False
    if w1 == w2:
        return False

    diff = []
    for i in range(len(w1)):
        if w1[i] != w2[i]:
            if w1[i] < w2[i]:
                pair = (w1[i], w2[i])
            else:
                pair = (w2[i], w1[i])
            diff.append(pair)

    if len(diff) == 1:
        if list(diff)[0] in SIMILAR:
            return True

def remove_similar(wordlist):
    stop_sim_check = False
    newlist = wordlist
    for w1 in wordlist:
        for w2 in wordlist:
            if similar_words(w1, w2):
                if wordfreq[w1] > wordfreq[w2]:
                    if w2 in newlist:
                        newlist.remove(w2)
                    if not w1 in newlist:
                        newlist.append(w1)
                    # print("Replace %s(%d) with %s(%d)" % (w2, wordfreq[w2], w1, wordfreq[w1]))
                    stop_sim_check = True
            if stop_sim_check:
                continue
    return newlist

def parselist():
    global wordfreq, wordtype
    # Read wordlist and list with banned words
    wf = open(DICTFILE, 'rb')
    wordsf = wf.readlines()
    wordsf.sort()
    words = []
    for w in wordsf:
        try:
            word = w.decode('utf-8')
        except:
            continue
        word = word.strip('\r\n')
        if len(word) < 3 or len(word) > 8:
            continue
        word = word.lower()
        for char in FORBIDDEN_CHARS:
            if word != word.replace(char,''):
                word = '__stop__'
                break
        if word == '__stop__':
            continue
        words.append(word)

    badwords = []
    if BADWORDSFILE:
        bad_wf = open(BADWORDSFILE, 'rb')
        badwordsf = bad_wf.readlines()
        for w in badwordsf:
            word = w.decode('utf-8')
            word = word.strip('\r\n')
            badwords.append(word)

    count = 0
    pword = ''
    newlist = []
    for word in words:
        if word in badwords:
            continue
        if not word in wordfreq:
            continue
        if word in wordtype and 'Vi' in wordtype[word]:
            if word[:-2] in newlist:
                continue
        elif word[-2:] == 'en' and word[:-2] in words:
            continue
        if word[-2:] == 'je' and word[:-2] in words:
            continue
        if word[-3:] == 'tje' and word[:-3] in words:
            continue
        if word[-2:] == 'dt' and word[:-1] in words:
            continue
        if word[:4] != pword[:4]:
            newlist.append(word)
            count += 1
        else:
            if wordfreq[word] > wordfreq[pword]:
                # print("Replace %s(%d) with %s(%d)" % (pword, wordfreq[pword], word, wordfreq[word]))
                newlist.pop()
                newlist.append(word)

        pword = word
    return newlist


if __name__ == '__main__':
    wordfreq = frequency()
    wordtype = wordtypes()
    wordlist = parselist()
    wordlist.sort()

    # wordlist = remove_similar(wordlist)

    print(wordlist)
    print(len(wordlist))

    f = open(OUTPUTFILE, 'w')
    for w in wordlist:
        f.write(w+'\r\n')
