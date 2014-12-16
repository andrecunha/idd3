# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division

import sys
sys.path.append('..')

import idd3
import nltk


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
