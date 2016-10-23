# -*- coding: utf-8 -*-
#
#    bip39-dutch-wordlist wordfreq
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

TYPEFILE = 'data/dutch-type.txt'
ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyz'

def wordtypes():
    wd = os.path.dirname(__file__)
    wt = {}
    with open('%s/%s' % (wd, TYPEFILE), 'r') as f:
        for l in f.readlines():
            f = l.split('/')
            if len(f[0]) < 3 or len(f[0]) > 8:
                continue
            foundstrangechar = False
            for char in f[0]:
                if char not in ALLOWED_CHARS:
                    foundstrangechar = True
            if foundstrangechar:
                continue
            try:
                wt.update({
                    f[0].lower(): f[1].replace('\n',''),
                })
            except:
                pass
    return wt

wordtype = wordtypes()
