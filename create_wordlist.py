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

import os
from wordfreq import wordfreq
from wordtype import wordtype

DICTFILE = 'data/dutch-norm.txt'
BADWORDSFILE = 'data/dutch-bad.txt'
WORDLISTDIR = 'wordlist'
OUTPUTFILE = 'dutch-output.txt'
SIMILAR = (
    ('a', 'e'), ('a', 'o'),
    ('b', 'd'), ('b', 'p'),
    ('c', 'k'), ('c', 's'),
    ('d', 'p'), ('d', 't'),
    ('e', 'i'), ('e', 'o'),
    ('f', 'v'),
    ('i', 'j'), ('i', 'y'),
    ('k', 'x'),
    ('m', 'n'), ('m', 'w'),
    ('n', 'u'),
    ('o', 'u'),
    ('s', 'x'), ('s', 'z'),
    ('u', 'v'), ('u', 'w'),
    ('v', 'w'),
)

workdir = os.path.dirname(__file__)


def similar_words(w1, w2):
    # Find words containing similar characters
    if len(w1) != len(w2):
        return False
    if w1 == w2:
        return False

    # Create list with character pairs from first and second word
    diff = []
    for i in range(len(w1)):
        if w1[i] != w2[i]:
            if w1[i] < w2[i]:
                pair = (w1[i], w2[i])
            else:
                pair = (w2[i], w1[i])
            diff.append(pair)

    # Check if character pair is found in SIMILAR constant pair list
    if len(diff) == 1:
        if list(diff)[0] in SIMILAR:
            return True
    return False

def remove_similar(wordlist):
    # Iterate through wordlist and remove words with similar characters and less frequency
    stop_sim_check = False
    newlist = wordlist
    for w1 in wordlist:
        for w2 in wordlist:
            if similar_words(w1, w2):
                if wordfreq[w1] > wordfreq[w2]:
                    wdel = w2
                    wnew = w1
                else:
                    wdel = w1
                    wnew = w2
                if wdel in newlist:
                    newlist.remove(wdel)
                if not wnew in newlist:
                    newlist.append(wnew)
                # print("Remove %s(%d), keep %s(%d)" % (wdel, wordfreq[wdel], wnew, wordfreq[wnew]))
                stop_sim_check = True
            if stop_sim_check:
                continue
    return newlist

def read_dictionary():
    global workdir
    wordlist = []
    wordprio = {}

    # Read words and priority from normalized dictionary file
    with open('%s/%s' % (workdir, DICTFILE), 'r') as f:
        dlines = [l for l in f.readlines()]
    for dl in dlines:
        fields = dl.split(',')
        if len(fields) != 4:
            raise ValueError("Unknown input line %s" % dl)
        wordlist.append(fields[0])
        wordprio.update({
            fields[0]: int(fields[2])
        })
    return wordlist, wordprio

def read_dictfile(file):
    global workdir
    if file:
        with open('%s/%s' % (workdir, file), 'rb') as f:
            return [l.decode('utf-8').strip() for l in f.readlines()]

def check_word(word, wordlist):
    suffixs = ['je', 'tje', 'jes', 'ste', 'te', 'dt', 's', 'e']
    for suf in suffixs:
        ls = len(suf)
        if word[-ls:]==suf and word[:-ls] in wordlist:
            # print("Keep %s and remove %s with suffix %s" % (word[:-ls], word, suf))
            return False
    return True

def first_word_better(word1, word2):
    # Returns true if the first word has a higher priority or word-frequency
    global wordprio, wordfreq
    if wordprio[word1] < wordprio[word2]:
        # print("Replace %s(%d) with %s(%d)" % (word2, wordfreq[word2], word1, wordfreq[word1]))
        return True
    elif wordfreq[word1] > wordfreq[word2]:
        # print("Replace %s(%d) with %s(%d)" % (word2, wordfreq[word2], word1, wordfreq[word1]))
        return True
    return False

def find_extra_words(wordlist, blacklist):
    print(len(wordtype))
    with open(WORDLISTDIR+'/'+OUTPUTFILE, 'r') as f:
        words = [w.strip() for w in f.readlines()]
    prefixes = [w[4:] for w in words]
    extrawords = []
    allowedtypes = ['Z','C','Yb','Vi','Aa','Ab']
    for nw in wordtype:
        if nw[:4] in prefixes:
            continue
        if nw in wordlist:
            continue
        if not nw in wordfreq or wordfreq[nw] < 100:
            continue
        if nw in badwords:
            continue
        if nw in blacklist:
            continue
        found_similar = False
        for w in words:
            if similar_words(nw, w):
                found_similar = True
                break
        if found_similar:
            continue
        if nw[-2:] == 'en':
            continue
        for type in allowedtypes:
            if type in wordtype[nw]:
                extrawords.append(nw)
                print(nw)
                break
    print(len(extrawords))

if __name__ == '__main__':
    wordlist, wordprio = read_dictionary()
    badwords = read_dictfile(BADWORDSFILE)
    otherwords = []
    for fd in os.listdir(workdir+'/'+WORDLISTDIR):
        if fd == OUTPUTFILE:
            continue
        else:
            with open('%s/wordlist/%s' % (workdir, fd), 'r') as f:
                otherwords += [w.strip() for w in f.readlines()]
    #
    # Use this method to generate extra words if you don't reach 2048
    # find_extra_words(wordlist, otherwords)
    # import sys; sys.exit()
    #
    count = 0
    pword = ''
    newlist = []
    for word in wordlist:
        if word in badwords:
            continue
        if word in otherwords:
            continue
        if not check_word(word, wordlist):
            continue
        # Ensure first 4 characters of a word are unique
        if word[:4] == pword[:4]:
            if first_word_better(word, pword):
                newlist.pop()
                newlist.append(word)
            else:
                continue
        else:
            newlist.append(word)
            count += 1
        pword = word

    newlist.sort()
    newlist = remove_similar(newlist)

    f = open(WORDLISTDIR+'/'+OUTPUTFILE, 'w')
    for w in newlist:
        f.write(w+'\r\n')

    print("Created wordlist with %d words" % len(newlist))
    print("Output writen to %s" % OUTPUTFILE)
