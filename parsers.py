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
import os
import nltk
from subprocess import call


class StanfordUnivDepParser(object):

    """An interface for the Stanford NN Dependency Parser, trained using
        the Universal Dependencies corpus."""

    def __init__(self, corenlp_path, model_path, pos_mapping_file_path):
        self.corenlp_path = corenlp_path
        self.model_path = model_path
        self.pos_mapping = self.load_mapping_file(pos_mapping_file_path)

    @staticmethod
    def load_mapping_file(path):
        mapping = {}
        with open(path, 'r') as mapping_file:
            for line in mapping_file.readlines():
                tags = line.strip().split('\t')
                mapping[tags[0]] = tags[1]

        return mapping

    @staticmethod
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

    def parse_raw_file(self, filename):
        stanford_run_cmd = ['java', '-mx1024m',
                            '-cp', self.corenlp_path + '/*:',
                            'edu.stanford.nlp.pipeline.StanfordCoreNLP',
                            '-annotators', 'tokenize,ssplit,pos,depparse',
                            '-depparse.model', self.model_path,
                            '-outputFormat', 'conll',
                            '-outputDirectory', '/tmp/', '-file', filename]

        call(stanford_run_cmd)

        self.normalize_file(os.path.basename(filename), self.pos_mapping)

        graphs = nltk.parse.dependencygraph.DependencyGraph.load(
            '/tmp/{0}.norm.conll'.format(os.path.basename(filename)))

        return graphs
