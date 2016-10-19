# -*- coding: utf-8 -*-
#
#    bip39-dutch-wordlist - Normalize List
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
import re


DICTFILES = [
    {
        'file': 'data/SONAR500.lemmaposfreqlist.1-gram.total.top5000.tsv',
        'struct': ['word','type','frequency'],
        'allowed-types': ['WW','N','ADJ'],
        'priority': 1,
    },
    {
        'file': 'data/dutch.txt',
        'struct': ['word'],
        'priority': 2,
    },
]

FORBIDDEN_CHARS = [' ', '-', '\'', '_', '.', ',']
OUTPUTFILE = 'wordlist/dutch-norm.txt'
MINFREQ = 2
MAXWORDS = 5000


def create_normalized():
    rebrackets = re.compile(".*?\((.*?)\)")

    wd = os.path.dirname(__file__)
    normdict = []
    wordcount = 0
    for dictio in DICTFILES:
        dictfile = dictio['file']
        with open('%s/%s' % (wd, dictfile), 'rb') as f:
            wordlist = [w.strip() for w in f.readlines()]
        for line in wordlist:
            wordcount += 1
            fields = line.split()
            data = {}
            i = 0
            for fld in dictio['struct']:
                fieldval = fields[i]
                try:
                    fieldval = fieldval.decode('utf-8')
                except:
                    print("Error decoding %s" % fieldval)
                    break
                if fld == 'word':
                    fieldval = fieldval.strip('\r\n')
                    if len(fieldval) < 3 or len(fieldval) > 8:
                        data = {}
                        break
                    fieldval = fieldval.lower()
                if fld == 'type':
                    typecom = re.findall(rebrackets, fieldval)[0]
                    fieldval = fieldval.replace("(" + typecom + ")","")
                    if fieldval not in dictio['allowed-types']:
                        data = {}
                        break
                data.update({
                    fld: fieldval
                })
                i += 1

            if data:
                normdict.append(data)

            if wordcount > MAXWORDS:
                from pprint import pprint
                pprint(normdict)
                import sys
                print(len(normdict))
                sys.exit()




if __name__ == '__main__':
    create_normalized()
