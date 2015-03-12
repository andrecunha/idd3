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
from idd3.rules.universal.np_rulesets import NounPhraseRuleset
from idd3.rules.universal.vp_rulesets import VerbPhraseRuleset
from idd3.rules.universal.adjp_rulesets import AdjectivalPhraseRuleset

import logging
logger = logging.getLogger(__name__)


class TopRuleset(Ruleset):

    """A dummy ruleset that starts the analysis process."""

    rel = 'TOP'

    def extract(self, relations, index, context, engine, info={}):
        return engine.analyze(relations, relations[index].deps[0], [index])


class ConjRuleset(NounPhraseRuleset, VerbPhraseRuleset):

    """A ruleset that processes the 'conj' relation."""

    rel = 'conj'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> list(str)
        OUTDATED

        This ruleset returns a list of strings, corresponding to the
            return_list value of NounPhraseRuleset.

        Examples:

            * Mary and John
                conj(Mary, John)
                -> return ['John']
        """

        if info['class'] == 'NP':
            logger.debug('ConjRuleset is processing node as NP')

            # TODO: Maybe just return the first element in the list.
            d = NounPhraseRuleset.extract(self, relations, index, context,
                                          engine)
            if d['ids_for_preconj'] == []:
                return d['return_list']
        elif info['class'] == 'VP':
            logger.debug('ConjRuleset is processing node as VP')

            d = VerbPhraseRuleset.extract(self, relations, index, context,
                                          engine, info)
            return d


class CompmodJoinRuleset(Ruleset):

    """A ruleset that processes the 'compmod-join' relation."""

    rel = 'compmod-join'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> str | list(str)

        An nn can be a single word or multiple words connected by cc/conj.

        Examples:

            * Oil prices
                nn(prices, Oil)
                -> return "Oil"
            * East and West Germany
                nn(Germany, East)
                cc(East, and)
                conj(East, West)
                -> return ["East", "West"]
        """
        conj_indices = Relation.get_children_with_dep('conj', relations,
                                                      index)

        if conj_indices != []:
            # Consume the conjunction.
            cc_indices = Relation.get_children_with_dep('cc', relations, index)
            for i in cc_indices:
                engine.analyze(relations, cc_indices[0], context + [index])

            conjs = [engine.analyze(relations, i, context + [index],
                                    info={'class': 'NP'})
                     for i in conj_indices]
            conjs = [c[0] for c in conjs]  # TODO: check if this makes sense.

            return [relations[index].word] + conjs
        else:
            return relations[index].word


class DetRuleset(Ruleset):

    """A ruleset that processes the 'det' relation."""

    rel = 'det'

    non_emitted_dets = ('the', 'a', 'an', 'this', 'these', 'that', 'those')

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> str | None

        A determiner may or may not emit a new proposition. Determiners like
            the, a, an, this, and these get joined to the noun they precede;
            others, like some and any, generate their own proposition.

        Examples:

            * The apple
                det(apple, The)
                -> return "The"

            * Some apples
                det(apple, some)
                -> emit((apple, some))
                -> return None
        """
        if relations[index].word.lower() in self.non_emitted_dets:
            return relations[index].word
        else:
            # TODO: maybe get the subject from info.
            engine.emit((relations[context[-1]].word, relations[index].word),
                        'M')
            return None


class AdpmodRuleset(Ruleset):

    """A ruleset that processes the 'adpmod' relation."""

    rel = 'adpmod'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> None

        Prepositional phrases always generate new propositions, according to
            Chand et al.'s manual.

        Examples:

            * to the city
                pobj(to, city)
                det(city, the)
                -> emit((to the city,))

            * to both East and West Germany
                pobj(to, Germany)
                preconj(Germany, both)
                nn(Germany, East)
                cc(East, and)
                conj(East, West)
                -> emit((to East Germany, )) # Proposition x
                -> emit((to West Germany, )) # Proposition y
                -> emit((both, x, y))

            * TODO: insert example with PCOMP.
        """
        # adpobj
        pobj_index = Relation.get_children_with_dep('adpobj', relations, index)
        if pobj_index != []:
            pobjs = engine.analyze(relations, pobj_index[0], context + [index])

            emitted_prop_ids = []
            for pobj in pobjs['return_list']:
                prop_id = engine.emit((relations[index].word + ' ' + pobj,),
                                      'M')
                emitted_prop_ids.append(prop_id)

            if pobjs['ids_for_preconj'] != []:
                indices = [j for i, j in enumerate(emitted_prop_ids)
                           if i in pobjs['ids_for_preconj']]
                proposition = tuple([pobjs['preconj']] + indices)
                engine.emit(proposition, 'C')

        # adpcomp
        pcomp_index = Relation.get_children_with_dep('adpcomp', relations,
                                                     index)
        if pcomp_index != []:
            pcomp = engine.analyze(relations, pcomp_index[0],
                                   context + [index])['return_value']
            if pcomp is not None:
                engine.emit((relations[index].word + ' ' + pcomp,), 'M')
            # TODO: check the 'else' condition.


class NumRuleset(Ruleset):

    """A ruleset that processes the 'num' relation."""

    rel = 'num'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> str

        Nummerical modifiers are treated in the same way as adjectives.
            This ruleset assembles and returns the number, and it's up
            to the calling NounPhraseRuleset to emit the propositions.
            This ruleset also emits propositions for quantifier phrase
            modifiers.

        Examples:

            * About 200 people
                num(people, 200)
                quantmod(200, About)
                -> emit((200, about)) # by calling QuantmodRuleset
                -> return "200"
        """
        number_indices = Relation.get_children_with_dep('num', relations, index)
        cc_indices = Relation.get_children_with_dep('cc',
                                                    relations, index)
        conj_indices = Relation.get_children_with_dep('conj',
                                                      relations, index)

        indices = sorted([index] + number_indices + cc_indices + conj_indices)

        words = []
        for n in indices:
            if n != index:
                word = engine.analyze(relations, n, context + [index],
                                      info={'class': 'NP'})
            else:
                word = relations[index].word

            if isinstance(word, str):
                words.append(word)
            elif isinstance(word, list):
                words += word

        this_number = ' '.join(words)

        # Process advmods
        advmod_indices = Relation.get_children_with_dep('advmod',
                                                        relations, index)
        for q in advmod_indices:
            engine.analyze(relations, q, context + [index],
                           {'num': this_number})

        return this_number


class WhatRuleset(NounPhraseRuleset, AdjectivalPhraseRuleset):

    """A ruleset that processes the 'what' relation."""

    rel = 'what'

    def extract(self, relations, index, context, engine, info={}):
        # if relations[index].tag in ('NN', 'NNS', 'NNP', 'NNPS'):
        if relations[index].ctag == 'NOUN':
            this = NounPhraseRuleset.extract(self, relations, index, context,
                                             engine, info)
            for noun in this['return_list']:
                engine.emit((noun,), 'WHAT')
        # elif relations[index].tag == 'JJ':
        elif relations[index].ctag == 'ADJ':
            this = AdjectivalPhraseRuleset.extract(self, relations, index,
                                                   context, engine, info)
            for adj in this:
                engine.emit((adj,), 'WHAT')
        else:
            # In case something weird happens, we just emit the word.
            engine.emit((relations[index].word,), 'WHAT')


class CompmodRuleset(Ruleset):

    """A ruleset that processes the 'compmod' relation."""

    rel = 'compmod'

    def extract(self, relations, index, context, engine, info={}):
        cc_indices = Relation.get_children_with_dep('cc', relations, index)

        if cc_indices != []:
            engine.analyze(relations, cc_indices[0], context + [index])
            conj_indices = Relation.get_children_with_dep('conj', relations,
                                                          index)
            conjs = [engine.analyze(relations, i, context + [index],
                                    info={'class': 'NP'})
                     for i in conj_indices]
            conjs = [c[0] for c in conjs]  # TODO: check if this makes sense.

            return [relations[index].word] + conjs
        else:
            return [relations[index].word]
