# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
import pprint
from idd3 import Relation, Engine
import rules


def demo():
    sent = [{'address': 0,
             'deps': [3],
             'rel': 'TOP',
             'tag': 'TOP',
             'word': None},
            {'address': 1,
             'deps': [],
             'head': 2,
             'rel': 'det',
             'tag': 'DT',
             'word': 'the'},
            {'address': 2,
             'deps': [1],
             'head': 3,
             'rel': 'nsubj',
             'tag': 'NN',
             'word': 'cat'},
            {'address': 3,
             'deps': [2],
             'head': 0,
             'rel': 'null',
             'tag': 'VBD',
             'word': 'ran'}]

    relations = []
    for word in sent:
        relations.append(Relation(**word))

    pprint.pprint(relations)

    rulesets = rules.all_rulesets
    engine = Engine(rulesets)
    engine.analyze(relations, 0)

    print(engine.props)


if __name__ == '__main__':
    demo()
