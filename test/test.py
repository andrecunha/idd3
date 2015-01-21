# -*- coding: utf-8 -*-
# IDD3 - Propositional Idea Density from Dependency Trees
# Copyright (C) 2014  Andre Luiz Verucci da Cunha
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, unicode_literals, division

import sys
sys.path.append('..')

import idd3
import nltk

import logging
logging.basicConfig(level=logging.INFO)


def test():
    with open('expected.txt', mode='r') as expected_file:
        expected = expected_file.readlines()

    up_to_index = len(expected)

    graphs = nltk.parse.dependencygraph.DependencyGraph.load('corpus.conll')

    engine = idd3.Engine(idd3.rules.all_rulesets,
                         idd3.transform.all_transformations)

    for i in range(up_to_index):
        relations = []
        for relation in graphs[i].nodelist:
            relations.append(idd3.Relation(**relation))

        engine.analyze(relations)
        props = engine.props

        exp = eval(expected[i])

        assert props == exp

        unprocessed_relations = engine.get_unprocessed_relations(relations)

        assert unprocessed_relations == []

if __name__ == '__main__':
    test()
