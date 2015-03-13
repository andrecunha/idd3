# -*- coding: utf-8 -*-
# IDD3 - Propositional Idea Density from Dependency Trees
# Copyright (C) 2014-2015  Andre Luiz Verucci da Cunha
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

import idd3
from idd3 import Relation, Engine
from idd3.rules import en, pt
import nltk
from sys import argv
from collections import defaultdict
from parsers import StanfordUnivDepParser, StanfordParser

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import os
_, columns = os.popen('stty size', 'r').read().split()

try:
    from termcolor import colored
    raise ImportError
except ImportError:
    def colored(string, color, attrs):
        return string


# Stanford NN dependency parser, trained using the normalized Penn Treebank.

# Change these variables to the path on your system
corenlp_path = os.path.expanduser('~') + \
    "/Develop/stanford_tools/corenlp"
model_path = 'data/nndep.model.txt.gz'
pos_mapping_file = 'data/ENGLISH-fine-to-universal.full.map'

# Traditional Stanford Parser with normalized output

# Change this variable to the path on your system
stanford_path = os.path.expanduser('~') + \
    "/Develop/stanford_tools/stanford-parser"


def get_sentence(graph):
    """Turns a graph into a list of words.
    """
    return ' '.join([node['word'] for node in graph.nodelist if node['word']])


def process_graphs(graphs):
    engine = Engine(idd3.all_rulesets, idd3.all_transformations)
    stats = defaultdict(int)

    for index in range(len(graphs)):
        print('-' * int(columns))
        relations = []
        for relation in graphs[index].nodelist:
            relations.append(Relation(**relation))

        print(colored('Sentence %d:' % (index + 1), 'white', attrs=['bold']))
        print('\t' + get_sentence(graphs[index]))

        print(colored('Propositions:', 'white', attrs=['bold']))
        try:
            engine.analyze(relations)
            for i, prop in enumerate(engine.props):
                print(str(i + 1) + ' ' + str(prop))
                stats[prop.kind] += 1
        except Exception as e:
            logger.error('{0} in engine.analyze: {1}'.format(
                e.__class__.__name__, e))

    print('-' * int(columns))
    return stats


def print_stats(stats):
    print('Stats:')
    print('Kind\t#\t')
    for kind, n in stats.items():
        print('{0}\t{1}'.format(kind, n))


def main():
    idd3.use_language(en)

    if len(argv) < 2:
        print('Usage: python', argv[0], '<input file>')
        return

    if argv[1].endswith('.conll'):
        graphs = nltk.parse.dependencygraph.DependencyGraph.load(argv[1])
    else:
        parser = StanfordUnivDepParser(corenlp_path, model_path,
                                       pos_mapping_file)

        # Uncomment for normalized Stanford Parser.
        # parser = StanfordParser(stanford_path, pos_mapping_file)

        graphs = parser.parse_raw_file(argv[1])

    stats = process_graphs(graphs)
    print_stats(stats)


if __name__ == '__main__':
    main()
