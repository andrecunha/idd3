# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Engine
import rules
import transform
import nltk


def test():
    with open('expected.txt', mode='r') as expected_file:
        expected = expected_file.readlines()

    up_to_index = len(expected)

    graphs = nltk.parse.dependencygraph.DependencyGraph.load('corpus.conll')

    engine = Engine(rules.all_rulesets, transform.all_transformations)

    for i in range(up_to_index):
        relations = []
        for relation in graphs[i].nodelist:
            relations.append(Relation(**relation))

        engine.analyze(relations)
        props = engine.props

        exp = eval(expected[i])

        assert props == exp

if __name__ == '__main__':
    test()
