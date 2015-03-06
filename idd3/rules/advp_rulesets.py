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
from idd3 import Relation, Ruleset


class AdverbialPhraseRuleset(Ruleset):

    """A base class for ADVP-like dependency substructures."""

    @staticmethod
    def process_nmod(relations, index, context, engine, info={}):

        """Process noun phrases as adverbial modifiers."""

        npadvmod_indices = Relation.get_children_with_dep('nmod',
                                                          relations, index)
        if npadvmod_indices != []:
            npadvmod = engine.analyze(relations, npadvmod_indices[0],
                                      context + [index])
            engine.emit((relations[index].word, npadvmod), 'M')

    @staticmethod
    def process_advmods(relations, index, context, engine, info={}):

        """Process adverbial modifiers (e.g., very slowly)."""

        advmod_indices = Relation.get_children_with_dep('advmod',
                                                        relations, index)
        for i in advmod_indices:
            advmod = engine.analyze(relations, i, context + [index],
                                    {'no_emit': True})
            engine.emit((relations[index].word, advmod), 'M')

    @staticmethod
    def process_adpmods(relations, index, context, engine, info):

        """Process adpositional modifiers."""

        prep_indices = Relation.get_children_with_dep('adpmod', relations,
                                                      index)
        for prep_index in prep_indices:
            engine.analyze(relations, prep_index, context + [index])

    def extract(self, relations, index, context, engine, info={}):
        if 'num' in info:
            # Advmod modifying number. Treat as quantmod.
            engine.emit((info['num'], relations[index].word), 'M')
            return (relations[index].word)

        self.process_nmod(relations, index, context, engine, info)

        self.process_advmods(relations, index, context, engine, info)

        self.process_adpmods(relations, index, context, engine, info)

        if 'no_emit' not in info:
            engine.emit((relations[index].word,), 'M')

        return (relations[index].word)


class AdvmodRuleset(AdverbialPhraseRuleset):

    """A ruleset that processes the 'advmod' relation."""

    rel = 'advmod'
