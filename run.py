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

from idd3 import Relation, Engine, rules, transform
import nltk
from sys import argv
from subprocess import call
from collections import defaultdict

import logging
logging.basicConfig(level=logging.INFO)

import os
_, columns = os.popen('stty size', 'r').read().split()

try:
    from termcolor import colored
    raise ImportError
except ImportError:
    def colored(string, color, attrs):
        return string


# MaltParser

# parser = nltk.parse.MaltParser(
#     working_dir="/home/andre/Develop/malt/maltparser-1.8",
#     mco="engmalt.linear-1.7",
#     additional_java_args=['-Xmx512m'])

# Stanford parser

# Change this variable to the path on your system
corenlp_path = os.path.expanduser('~') + \
    "/Develop/stanford_tools/corenlp"
stanford_run_cmd = ['java', '-mx1024m', '-cp', corenlp_path + '/*:',
                    'edu.stanford.nlp.pipeline.StanfordCoreNLP',
                    '-annotators', 'tokenize,ssplit,pos,depparse',
                    '-depparse.model', './data/nndep.model.txt.gz',
                    '-outputFormat', 'conll',
                    '-outputDirectory', '/tmp/', '-file', '-']


def load_mapping_file(path):
    mapping = {}
    with open(path, 'r') as mapping_file:
        for line in mapping_file.readlines():
            tags = line.strip().split('\t')
            mapping[tags[0]] = tags[1]

    return mapping


def normalize_file(infilename, pos_mapping):
    with open('/tmp/{0}.conll'.format(infilename), 'r') as infile, \
            open('/tmp/{0}.norm.conll'.format(infilename), 'w') as outfile:
        for line in infile.readlines():
            if not line or line.isspace():
                outfile.write(line)
            else:
                entries = [entry.strip() for entry in line.split('\t')]
                outfile.write('\t'.join([entries[0],
                                         entries[1],
                                         entries[2],
                                         pos_mapping[entries[3]],
                                         entries[3],
                                         entries[4],
                                         entries[5],
                                         entries[6],
                                         '_',
                                         '_',
                                         ]) + '\n')


def get_sentence(graph):
    """Turns a graph into a list of words.
    """
    return ' '.join([node['word'] for node in graph.nodelist if node['word']])


def process_graphs(graphs):
    engine = Engine(rules.all_rulesets, transform.all_transformations)
    stats = defaultdict(int)

    for index in range(len(graphs) - 1):
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
        except Exception:
            pass

    print('-' * int(columns))
    return stats


def print_stats(stats):
    print('Stats:')
    print('Kind\t#\t')
    for kind, n in stats.items():
        print('{0}\t{1}'.format(kind, n))


def main():
    if len(argv) < 2:
        print('Usage: python', argv[0], '<input file>')
        return

    pos_mapping = load_mapping_file('data/ENGLISH-fine-to-universal.full.map')

    if argv[1].endswith('.conll'):
        graphs = nltk.parse.dependencygraph.DependencyGraph.load(argv[1])
    else:
        # tagged_sents = [nltk.pos_tag(nltk.word_tokenize(sent))
        #                 for sent in sents]

        # graphs = parser.tagged_parse_sents(tagged_sents)

        stanford_run_cmd[-1] = argv[1]
        call(stanford_run_cmd)
        normalize_file(os.path.basename(argv[1]), pos_mapping)

        graphs = nltk.parse.dependencygraph.DependencyGraph.load(
            '/tmp/{0}.norm.conll'.format(os.path.basename(argv[1])))

    stats = process_graphs(graphs)
    print_stats(stats)


if __name__ == '__main__':
    main()
