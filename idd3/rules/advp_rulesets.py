# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Ruleset


class AdverbialPhraseRuleset(Ruleset):

    """A base class for ADVP-like dependency substructures."""

    @staticmethod
    def process_npadvmod(relations, index, context, engine, info={}):

        """TODO: Docstring for process_npadvmod."""

        npadvmod_indices = Relation.get_children_with_dep('npadvmod',
                                                          relations, index)
        if npadvmod_indices != []:
            npadvmod = engine.analyze(relations, npadvmod_indices[0],
                                      context + [index])
            engine.emit((relations[index].word, npadvmod))

    @staticmethod
    def process_advmods(relations, index, context, engine, info={}):

        """TODO: Docstring for process_advmods."""

        advmod_indices = Relation.get_children_with_dep('advmod',
                                                        relations, index)
        for i in advmod_indices:
            advmod = engine.analyze(relations, i, context + [index],
                                    {'no_emit': True})
            engine.emit((relations[index].word, advmod))

    @staticmethod
    def process_preps(relations, index, context, engine, info):

        """TODO: Docstring for process_preps."""

        prep_indices = Relation.get_children_with_dep('prep', relations, index)
        for prep_index in prep_indices:
            engine.analyze(relations, prep_index, context + [index])

    def extract(self, relations, index, context, engine, info={}):
        self.process_npadvmod(relations, index, context, engine, info)

        self.process_advmods(relations, index, context, engine, info)

        self.process_preps(relations, index, context, engine, info)

        if 'no_emit' not in info:
            engine.emit((relations[index].word,))

        return (relations[index].word)


class AdvmodRuleset(AdverbialPhraseRuleset):

    """A ruleset that processes the 'advmod' relation."""

    rel = 'advmod'