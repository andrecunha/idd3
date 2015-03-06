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
import pprint
from idd3 import Relation, Engine, rules, transform
import nltk
from sys import argv

import logging
logging.basicConfig(level=logging.DEBUG)

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
    for i, prop in enumerate(engine.props):
        print(str(i + 1) + ' ' + str(prop))

    print(colored('Unprocessed relations:', 'white', attrs=['bold']))
    for relation in engine.get_unprocessed_relations(relations):
        print(relation)

if __name__ == '__main__':
    if len(argv) != 3:
        print('Usage: python', argv[0], '<conll file>', '<index>')
    else:
        demo()
