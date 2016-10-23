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
import unittest

DICTFILE = 'dutch-output.txt'

workdir = os.path.dirname(__file__)

class WordlistTest(unittest.TestCase):

    def setUp(self):
        with open('%s/wordlist/%s' % (workdir, DICTFILE), 'r') as f:
            self.words = [w.strip() for w in f.readlines()]

    def test_collision(self):
        problems = 0
        for fd in os.listdir(workdir+'/'+'wordlist'):
            if fd == DICTFILE:
                continue
            # For now only check English
            # if fd != 'english.txt':
            #     continue
            with open('%s/wordlist/%s' % (workdir, fd), 'r') as f:
                wordsfor = [w.strip() for w in f.readlines()]
                for word in self.words:
                    if word in wordsfor:
                        print("Word '%s' also found in %s dictionary" % (word, fd))
                        problems += 1
        self.assertEqual(problems, 0)

    def test_wordslengths(self):
        words = [w for w in self.words if len(w) < 3 or len(w) > 8]
        self.assertListEqual(words, [])

    def test_dict_size(self):
        self.assertEqual(len(self.words), 2048)

    def test_validchars(self):
        letters = set(sum([list(w) for w in self.words], []))
        for l in letters:
            self.assertIn(l, 'abcdefghijklmnopqrstuvwxyz')

    def test_sorted_unique(self):
        unique = list(set(self.words))
        unique.sort()
        self.assertListEqual(unique, self.words)

    def test_word_prefix(self):
        pword = ''
        problems = 0
        for word in self.words:
            if word[:4] == pword[:4]:
                print("Duplicate prefix for %s and %s" % (word, pword))
                problems += 1
            pword = word
        self.assertEqual(problems, 0)

    def test_similarity(self):
        similar = (
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
        # (
        #     ('a', 'c'), ('a', 'e'), ('a', 'o'),
        #     ('b', 'd'), ('b', 'h'), ('b', 'p'), ('b', 'q'), ('b', 'r'),
        #     ('c', 'e'), ('c', 'g'), ('c', 'n'), ('c', 'o'), ('c', 'q'), ('c', 'u'),
        #     ('d', 'g'), ('d', 'h'), ('d', 'o'), ('d', 'p'), ('d', 'q'),
        #     ('e', 'f'), ('e', 'o'),
        #     ('f', 'i'), ('f', 'j'), ('f', 'l'), ('f', 'p'), ('f', 't'),
        #     ('g', 'j'), ('g', 'o'), ('g', 'p'), ('g', 'q'), ('g', 'y'),
        #     ('h', 'k'), ('h', 'l'), ('h', 'm'), ('h', 'n'), ('h', 'r'),
        #     ('i', 'j'), ('i', 'l'), ('i', 't'), ('i', 'y'),
        #     ('j', 'l'), ('j', 'p'), ('j', 'q'), ('j', 'y'),
        #     ('k', 'x'),
        #     ('l', 't'),
        #     ('m', 'n'), ('m', 'w'),
        #     ('n', 'u'), ('n', 'z'),
        #     ('o', 'p'), ('o', 'q'), ('o', 'u'), ('o', 'v'),
        #     ('p', 'q'), ('p', 'r'),
        #     ('q', 'y'),
        #     ('s', 'z'),
        #     ('u', 'v'), ('u', 'w'), ('u', 'y'),
        #     ('v', 'w'), ('v', 'y')
        # )

        fail = False

        for w1 in self.words:
            for w2 in self.words:
                if len(w1) != len(w2):
                    continue

                if w1 == w2:
                    continue

                if w1 > w2:
                    # No need to print warning twice
                    continue

                diff = []
                for i in range(len(w1)):
                    if w1[i] != w2[i]:
                        if w1[i] < w2[i]:
                            pair = (w1[i], w2[i])
                        else:
                            pair = (w2[i], w1[i])

                        diff.append(pair)

                if len(diff) == 1:
                    if list(diff)[0] in similar:
                        fail = True
                        print("Similar words: %s, %s" % (w1, w2))

        if fail:
            self.fail("Similar words found")


def __main__():
    unittest.main()

if __name__ == "__main__":
    __main__()
