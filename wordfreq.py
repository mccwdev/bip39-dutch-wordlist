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

FREQFILE = 'data/dutch-frequency.txt'


def frequency():
    wd = os.path.dirname(__file__)
    with open('%s/%s' % (wd, FREQFILE), 'r') as f:
        return [w.split('\t') for w in f.readlines()]

wordfreq = frequency()