# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
import rules
import pprint


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
            'null' in case of element pointed to by ROOT).
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


class Ruleset(object):
    """A ruleset is responsible for processing edges of a certain label."""

    def __init__(self, rel):
        """Form a ruleset.

        :rel: the label of the relation this ruleset handles.
        """
        self.rel = rel
        pass

    def applies(self, rel):
        """Check whether this ruleset applies to a particular relation.

        :rel: the relation label.
        :returns: True if this ruleset applies to the relation; false otherwise.

        """
        return rel == self.rel

    def extract(self, relations, index, context, engine):
        """Extract the corresponding propositions from a relation.

        :relations: the list of relations in a sentence.
        :index: the index of the relation to be processed.
        :context: a list of indices representing the path from the TOP node
            to the current one.
        :engine: the engine that is running the analysis process.
        :returns: a string representation that can be embedded in other
            propositions.

        """
        raise "Don't instantiate Ruleset. Use a subclass instead."


class Engine(object):
    """An engine is responsible for running the analysis process, by calling the
        right rulesets and collecting the emitted propositions."""

    def __init__(self, rulesets):
        """Form an engine.

        :rulesets: a list of the rulesets to be used.
        """
        self.rulesets = rulesets

    def _build_rulesets_dict(self, relations):
        """Creates a dictionary associating relation labels to their
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
                print('WARNING: Unrecognized relation ' + relation.rel)

            self._rulesets_dict[relation.rel] = ruleset

    def emit(self, prop):
        """Emits a new proposition, storing it in this instance's
            'props' attribute.

        :prop: the proposition to be emitted.
        """
        self.props.append(prop)

    def analyze(self, relations, index, context=[]):
        """Analyzes a sentence, using this instance's ruleset set.

        :relations: the relations in a sentence.
        :index: the index of the relation to be analyzed.
        :returns: the return value of the corresponding ruleset's extract
            method.
        """
        # Clear results from previous executions and prepare for starting.
        if relations[index].rel == 'TOP':
            self.props = []
            self._build_rulesets_dict(relations)

        return self._rulesets_dict[relations[index].rel]\
            .extract(relations, index, context, self)


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


if __name__ == '__main__':
    demo()
