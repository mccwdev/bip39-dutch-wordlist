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
BADWORDSFILE = 'wordlist/dutch-bad.txt'
FORBIDDEN_CHARS = [' ', '-', '.', ',']
OUTPUTFILE = 'wordlist/dutch-bip39.txt'

wordfreq = {}

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


def parselist():
    global wordfreq
    # Read wordlist and list with banned words
    wf = open(DICTFILE, 'rb')
    words = wf.readlines()
    words.sort()
    badwords = []
    if BADWORDSFILE:
        bad_wf = open(BADWORDSFILE, 'rb')
        badwordsb = bad_wf.readlines()
        for bw in badwordsb:
            bword = bw.decode('utf-8')
            bword = bword.strip('\r\n')
            badwords.append(bword)

    count = 0
    pword = ''
    newlist = []
    for w in words:
        try:
            word = w.decode('utf-8')
            word = word.strip('\r\n')
            if len(word) < 3 or len(word) > 8:
                continue
            for char in FORBIDDEN_CHARS:
                if word != word.replace(char,''):
                    word = '__stop__'
                    break
            if word == '__stop__':
                continue
            word = word.lower()
            if word in badwords:
                continue
            if word[:4] != pword[:4]:
                newlist.append(word)
                count += 1
            else:
                if not word in wordfreq:
                    continue
                if wordfreq[word] > wordfreq[pword]:
                    # print("Replace %s(%d) with %s(%d)" % (pword, wordfreq[pword], word, wordfreq[word]))
                    newlist.pop()
                    newlist.append(word)

            pword = word
        except:
            continue
    print(count)
    return newlist


if __name__ == '__main__':
    wordfreq = frequency()
    wordlist = parselist()
    wordlist.sort()
    print(wordlist)

    f = open(OUTPUTFILE, 'w')
    for w in wordlist:
        f.write(w+'\r\n')
