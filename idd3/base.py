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

import logging
logger = logging.getLogger(__name__)


class Relation(object):
    """Represents a relation in the dependency tree."""

    def __init__(self, **kwargs):
        """Form a relation.

        :address: the index of the word in the sentence, starting at 1 (0 in
            case of the ROOT relation).
        :deps: an array containing the indexes of the words whose root is the
            corresponding word.
        :head: the head of this relation (None, in case of ROOT).
        :rel: the relation label (e.g., nsubj, det. 'TOP' in case of ROOT;
            'null' or 'root' in case of element pointed to by ROOT).
        :tag: PoS-tag of the corresponding word ('TOP' in case of ROOT).
        :word: the corresponding word (None in case of ROOT).
        """
        self.address = kwargs['address']
        self.deps = kwargs['deps']
        if 'head' in kwargs:
            self.head = kwargs['head']
        else:
            self.head = None
        self.rel = kwargs['rel']
        self.tag = kwargs['tag']
        self.word = kwargs['word']

    @staticmethod
    def get_children_with_dep(rel, relations, index):
        """Check whether the corresponding word has children in the tree
            connected to it through a relation of a certain label, returning
            the indices of the other relations if they exist, and an empty list
            otherwise.

        :rel: the label of the potential child relation.
        :relations: all the relations of the sentence.
        :index: index of the current relation.
        :returns: a list containing the indices of a relation connected to this
            one through the 'dep' label if they exist, and an empty list
            otherwise.

        """
        return [child_index for child_index in relations[index].deps
                if relations[child_index].rel == rel
                and relations[child_index].head == index]

    def __repr__(self):
        keys = sorted(self.__dict__)

        string = '{'
        for k, key in enumerate(keys):
            string += '{key}: {value}'.format(key=key,
                                              value=self.__dict__[key])
            if k != len(keys) - 1:
                string += ', '
        string += '}'

        return string


class Proposition(object):

    """Represents a proposition, with its content and kind."""

    def __init__(self, content, kind):
        """Form a proposition

        :content: the content of the proposition. E.g.: (ran, the cat).
        :kind: the kind of the proposition. E.g., P (predication),
        M (modification), C (connection), and so on.

        """
        self.content = content
        self.kind = kind

    def __repr__(self):
        _prop = []
        for w in self.content:
            if isinstance(w, str):
                _prop.append(w)
            else:
                _prop.append(str(w))

        content = ', '.join(_prop)
        return '{0} [{1}]'.format(content, self.kind)


class Transformation(object):
    """Transforms a given dependency tree to facilitate its processing."""

    def transform(self, relations):
        """Apply the corresponding transformation in place.

        :relations: the list of relations in a sentence.
        """
        raise "Don't instantiate Transformation. Use a subclass instead."


class Ruleset(object):
    """A ruleset is responsible for processing relations of a certain label."""

    def applies(self, rel):
        """Check whether this ruleset applies to a particular relation.

        :rel: the relation label.
        :returns: True if this ruleset applies to the relation; false otherwise.

        """
        return rel == self.rel

    def extract(self, relations, index, context, engine, info={}):
        """Extract the corresponding propositions from a relation.

        :relations: the list of relations in a sentence.
        :index: the index of the relation to be processed.
        :context: a list of indices representing the path from the TOP node
            to the current one.
        :engine: the engine that is running the analysis process.
        :info: a dictionary containing already parsed contextual information.
        :returns: a string representation that can be embedded in other
            propositions.

        """
        raise "Don't instantiate Ruleset. Use a subclass instead."


class Engine(object):
    """An engine is responsible for running the analysis process, by calling the
        right rulesets and collecting the emitted propositions."""

    def __init__(self, rulesets, transformations=[]):
        """Form an engine.

        :rulesets: a list of the rulesets to be used.
        :transformations: a list of transformations to be applied to the
            sentences prior to processing.
        """
        self.rulesets = rulesets
        self.transformations = transformations

    def _build_rulesets_dict(self, relations):
        """Create a dictionary associating relation labels to their
            corresponding ruleset instance.

        :relations: the list of relations in a sentence.
        """
        self._rulesets_dict = {}

        for relation in relations:
            ruleset = None
            for _ruleset in self.rulesets:
                if _ruleset.applies(relation.rel):
                    ruleset = _ruleset
                    break
            if ruleset is None:
                logger.warning('Unrecognized relation %s.', relation.rel)

            self._rulesets_dict[relation.rel] = ruleset

    def emit(self, prop, kind='PROP'):
        """Emit a new proposition, storing it in this instance's
            'props' attribute.

        :prop: the proposition to be emitted.
        """
        self.props.append(Proposition(prop, kind))
        return len(self.props)

    @staticmethod
    def mark_processed(relations, index):
        """Mark a relation as processed.

        :relations: the list of relations.
        :index: the index of the relation to be marked as processed.
        """
        relations[index].processed = True

    def analyze(self, relations, index=0, context=[], info={}):
        """Analyze a sentence, using this instance's ruleset set.

        :relations: the relations in a sentence.
        :index: the index of the relation to be analyzed.
        :context: the path from the TOP relation to the current one.
        :info: a dictionary containing already parsed contextual information.
        :returns: the return value of the corresponding ruleset's extract
            method.
        """
        # Clear results from previous executions, apply transformations,
        #   and prepare for starting.
        if relations[index].rel == 'TOP':
            for transformation in self.transformations:
                transformation.transform(relations)

            from pprint import pformat
            logger.debug('After transformations:\n%s', pformat(relations))

            self.props = []
            for relation in relations:
                relation.processed = False
            self._build_rulesets_dict(relations)

        logger.debug('Will call ruleset %s from caller %d',
                     self._rulesets_dict[relations[index].rel]
                     .__class__.__name__,
                     context[-1] if len(context) > 0 else -1)

        value = self._rulesets_dict[relations[index].rel]\
            .extract(relations, index, context, self, info)

        self.mark_processed(relations, index)

        return value

    @staticmethod
    def get_unprocessed_relations(relations):
        return [relation for relation in relations if not relation.processed]
