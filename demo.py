# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
import pprint
from idd3 import Relation, Engine, rules, transform
import nltk
from sys import argv

try:
    from termcolor import colored
except ImportError:
    def colored(string, color, attrs):
        return string


def demo():
    graphs = nltk.parse.dependencygraph.DependencyGraph.load(argv[1])
    index = int(argv[2]) - 1

    engine = Engine(rules.all_rulesets, transform.all_transformations)

    relations = []
    for relation in graphs[index].nodelist:
        relations.append(Relation(**relation))

    print(colored('Sentence %d:' % (index + 1), 'white', attrs=['bold']))
    pprint.pprint(relations)

    print(colored('Propositions:', 'white', attrs=['bold']))
    engine.analyze(relations)
    pprint.pprint(engine.props)

    print(colored('Unprocessed relations:', 'white', attrs=['bold']))
    for relation in engine.get_unprocessed_relations(relations):
        print(relation)

if __name__ == '__main__':
    if len(argv) != 3:
        print('Usage: python', argv[0], '<conll file>', '<index>')
    else:
        demo()
