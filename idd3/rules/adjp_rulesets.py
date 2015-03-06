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
from idd3 import Relation, Ruleset


class AdjectivalPhraseRuleset(Ruleset):

    """A base class for AdjP-like dependency substructures."""

    @staticmethod
    def process_advmods(relations, index, context, engine, info={}):

        """Process adverbial modifiers (e.g., very difficult)."""

        advmod_indices = Relation.get_children_with_dep('advmod', relations,
                                                        index)
        advmods = [engine.analyze(relations, i, context + [index],
                                  {'no_emit': True})
                   for i in advmod_indices]

        return advmods

    @staticmethod
    def process_xcomp(relations, index, context, engine, info={}):

        """Process reduced clausal modifiers (e.g., hard to imagine)."""

        xcomp_indices = Relation.get_children_with_dep('xcomp', relations,
                                                       index)
        for i in xcomp_indices:
            if 'subj' not in info:
                info['subj'] = {'return_list': ['NO_SUBJ'],
                                'rcmod_wdt': None}
            engine.analyze(relations, i, context + [index], info)

    @staticmethod
    def process_adpmods(relations, index, context, engine, info):

        """Process adpositional modifiers (e.g., angry with you)."""

        prep_indices = Relation.get_children_with_dep('adpmod', relations,
                                                      index)
        for prep_index in prep_indices:
            engine.analyze(relations, prep_index, context + [index])

    def extract(self, relations, index, context, engine, info={}):
        advmods = AdjectivalPhraseRuleset.process_advmods(relations, index,
                                                          context, engine, info)

        AdjectivalPhraseRuleset.process_xcomp(relations, index,
                                              context, engine, info)

        AdjectivalPhraseRuleset.process_adpmods(relations, index,
                                                context, engine, info)

        # TODO: Add cc/conj handling.
        this = [relations[index].word]

        for advmod in advmods:
            for word in this:
                engine.emit((word, advmod), 'M')

        return this


class AcompRuleset(AdjectivalPhraseRuleset):

    """A ruleset that processes the 'acomp' relation."""

    rel = 'acomp'


class AmodRuleset(AdjectivalPhraseRuleset):

    """A ruleset that processes the 'amod' relation."""

    rel = 'amod'
