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
from os.path import basename
import nltk
from subprocess import call


def load_mapping_file(path):
        mapping = {}
        with open(path, 'r') as mapping_file:
            for line in mapping_file.readlines():
                tags = line.strip().split('\t')
                mapping[tags[0]] = tags[1]

        return mapping


class StanfordUnivDepParser(object):

    """An interface for the Stanford NN Dependency Parser, trained using
        the Universal Dependencies corpus."""

    def __init__(self, corenlp_path, model_path, pos_mapping_file_path):
        self.corenlp_path = corenlp_path
        self.model_path = model_path
        self.pos_mapping = load_mapping_file(pos_mapping_file_path)

    def normalize_file(self, pos_mapping):
        with open(self.conll_file_path, 'r') as infile, \
                open(self.norm_file_path, 'w') as outfile:
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

    def parse_raw_file(self, filename):
        self.conll_file_path = '/tmp/{0}.conll'.format(basename(filename))
        self.norm_file_path = '/tmp/{0}.norm.conll'.format(basename(filename))

        stanford_run_cmd = ['java', '-mx1024m',
                            '-cp', self.corenlp_path + '/*:',
                            'edu.stanford.nlp.pipeline.StanfordCoreNLP',
                            '-annotators', 'tokenize,ssplit,pos,depparse',
                            '-depparse.model', self.model_path,
                            '-outputFormat', 'conll',
                            '-outputDirectory', '/tmp/', '-file', filename]

        call(stanford_run_cmd)

        self.normalize_file(self.pos_mapping)

        graphs = nltk.parse.dependencygraph.DependencyGraph.load(
            self.norm_file_path)

        if len(graphs) and len(graphs[-1].nodelist) == 1:
            del graphs[-1]

        return graphs


class StanfordParser(object):

    """An interface for the Stanford Parser with default Stanford
        Dependencies."""

    def __init__(self, stanford_path, pos_mapping_file_path):
        self.stanford_path = stanford_path
        self.pos_mapping = load_mapping_file(pos_mapping_file_path)

    @staticmethod
    def get_normalized_word(node):
        if not node['word']:
            return node['word']

        word = node['word']

        if word == '-LRB-':
            word = '('
        elif word == '-RRB-':
            word = ')'
        elif word == '-LCB-':
            word = '{'
        elif word == '-RCB-':
            word = '}'
        elif word == '-LSB-':
            word = '['
        elif word == '-RSB-':
            word = ']'

        return word

    @staticmethod
    def get_normalized_label(node):
        label = node['rel']
        ctag = node['ctag']

        if label == 'null':
            label = 'ROOT'
        elif label == 'root':
            label = 'ROOT'
        elif label == 'punct':
            label = 'p'
        elif label == 'possessive':
            label = 'adp'
        elif label == 'abbrev':
            label = 'appos'
        elif label == 'number':
            label = 'num'
        elif label == 'npadvmod':
            label = 'nmod'
        elif label == 'prep':
            label = 'adpmod'
        elif label == 'pobj':
            label = 'adpobj'
        elif label == 'pcomp':
            label = 'adpcomp'
        elif label == 'purpcl':
            label = 'advcl'
        elif label == 'tmod':
            if ctag == 'NOUN' or ctag == 'NUM' or ctag == 'PRON' or ctag == 'X':
                label = 'nmod'
            elif ctag == 'ADV':
                label = 'advmod'
            elif ctag == 'ADJ':
                label = 'amod'
            elif ctag == 'ADP':
                label = 'adpmod'
            elif ctag == 'VERB':
                label = 'advcl'
        elif label == 'quantmod':
            label = 'advmod'
        elif label == 'complm':
            label = 'mark'
        elif label == 'predet':
            label = 'det'
        elif label == 'preconj':
            label = 'cc'
        elif label == 'nn':
            label = 'compmod'
        elif label == 'ps':
            label = 'adp'

        return label

    @staticmethod
    def get_normalized_tag(node):
        tag = node['tag']
        word = node['word']
        label = node['tag']

        if tag == '-LRB-':
            tag = '('
        elif tag == '-RRB-':
            tag = ')'
        elif tag == ('TO') and word.lower() == 'to':
            tag = 'IN'

        # Fix up incorrect 'to' particles
        if tag == 'IN' and word.lower() == 'to'\
                and label in ('aux', 'xcomp', 'ccomp'):
            tag = 'TO'

        return tag

    def normalize_file(self):
        graphs = nltk.parse.dependencygraph.DependencyGraph.load(
            self.conll_file_path)

        if len(graphs) and len(graphs[-1].nodelist) == 1:
            del graphs[-1]

        for graph in graphs:
            for node in graph.nodelist:
                node['word'] = self.get_normalized_word(node)
                node['rel'] = self.get_normalized_label(node)
                node['tag'] = self.get_normalized_tag(node)
                node['ctag'] = self.pos_mapping[node['tag']]\
                    if node['tag'] != 'TOP' else node['ctag']

        with open(self.norm_file_path, 'w') as outputfile:
            for graph in graphs:
                outputfile.write(graph.to_conll(10) + '\n')

    def parse_raw_file(self, filename):
        self.tree_file_path = '/tmp/{0}.tree'.format(basename(filename))
        self.conll_file_path = '/tmp/{0}.conll'.format(basename(filename))
        self.norm_file_path = '/tmp/{0}.norm.conll'.format(basename(filename))

        run_cmd = ['java', '-mx1024m',
                   '-cp', self.stanford_path + '/*:',
                   'edu.stanford.nlp.parser.lexparser.LexicalizedParser',
                   '-outputFormat', 'penn',
                   'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz',
                   filename]
        convert_tree_cmd = ['java', '-mx1024m',
                            '-cp', self.stanford_path + '/*:',
                            'edu.stanford.nlp.trees.EnglishGrammaticalStructure',
                            '-conllx', '-basic', '-makeCopulaHead', '-keepPunct',
                            '-treeFile', self.tree_file_path]

        with open(self.tree_file_path, mode='w') as tree_file,\
                open(self.conll_file_path, mode='w') as conll_file:
            call(run_cmd, stdout=tree_file)
            call(convert_tree_cmd, stdout=conll_file)

        self.normalize_file()

        graphs = nltk.parse.dependencygraph.DependencyGraph.load(
            self.norm_file_path)

        if len(graphs) and len(graphs[-1].nodelist) == 1:
            del graphs[-1]

        return graphs
