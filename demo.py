# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
import pprint
from idd3 import Relation, Engine
import rules
import nltk
from sys import argv


def demo():
    graphs = nltk.parse.dependencygraph.DependencyGraph.load(argv[1])
    up_to_index = int(argv[2])

    engine = Engine(rules.all_rulesets)

    for i in range(up_to_index):
        relations = []
        for relation in graphs[i].nodelist:
            relations.append(Relation(**relation))

        pprint.pprint(relations)

        engine.analyze(relations)

        pprint.pprint(engine.props)


if __name__ == '__main__':
    if len(argv) != 3:
        print('Usage: python', argv[0], '<conll file>', '<up to index>')
    else:
        demo()
