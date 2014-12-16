# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Ruleset


class AdjectivalPhraseRuleset(Ruleset):

    """A base class for AdjP-like dependency substructures."""

    @staticmethod
    def process_advmods(relations, index, context, engine, info={}):

        """TODO: Docstring for process_advmods."""

        advmod_indices = Relation.get_children_with_dep('advmod', relations,
                                                        index)
        advmods = [engine.analyze(relations, i, context + [index],
                                  {'no_emit': True})
                   for i in advmod_indices]

        return advmods

    @staticmethod
    def process_xcomp(relations, index, context, engine, info={}):

        """TODO: Docstring for process_xcomp."""

        xcomp_indices = Relation.get_children_with_dep('xcomp', relations,
                                                       index)
        for i in xcomp_indices:
            engine.analyze(relations, i, context + [index], {'subj': 'NO_SUBJ'})

    def extract(self, relations, index, context, engine, info={}):
        advmods = AdjectivalPhraseRuleset.process_advmods(relations, index,
                                                          context, engine, info)

        AdjectivalPhraseRuleset.process_xcomp(relations, index,
                                              context, engine, info)

        # TODO: Add cc/conj handling.
        this = [relations[index].word]

        for advmod in advmods:
            for word in this:
                engine.emit((word, advmod))

        return this


class AcompRuleset(AdjectivalPhraseRuleset):

    """A ruleset that processes the 'acomp' relation."""

    rel = 'acomp'


class AmodRuleset(AdjectivalPhraseRuleset):

    """A ruleset that processes the 'amod' relation."""

    rel = 'amod'