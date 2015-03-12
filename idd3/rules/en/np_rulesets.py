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
from idd3.base import Relation
from idd3.rules import universal

import logging
logger = logging.getLogger(__name__)


class NounPhraseRuleset(universal.np_rulesets.NounPhraseRuleset):

    @staticmethod
    def handle_np_with_of_phrase(relations, index, context, engine, info={}):

        """Handle noun phrases that start with 'of' phrases, such as
            'some of'."""

        prep_index = Relation.get_children_with_dep('adpmod', relations,
                                                    index)[0]
        pobj_index = Relation.get_children_with_dep('adpobj', relations,
                                                    prep_index)[0]

        pobj_return_value = engine.analyze(relations, pobj_index, context +
                                           [index, prep_index])

        for noun in pobj_return_value['return_list']:
            engine.emit((noun, relations[index].word + ' ' +
                         relations[prep_index].word), 'M')

        engine.mark_processed(relations, prep_index)

        return pobj_return_value

    def extract(self, relations, index, context, engine, info={}):
        if relations[index].word.lower() in ('some', 'kind') and\
                relations[relations[index].deps[0]].rel == 'adpmod':
            return self.handle_np_with_of_phrase(relations, index, context,
                                                 engine, info)

        return super(NounPhraseRuleset, self).extract(relations, index,
                                                      context, engine, info)


class NsubjRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'nsubj' relation."""

    rel = 'nsubj'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> list(str)
        OUTDATED

        This ruleset returns a list of strings, corresponding to the
            return_list value of NounPhraseRuleset.

        Examples:

            * The man was sitting in the park.
                nsubj(sitting, man)
                det(man, the)
                -> return ['the man']

            * Mary and John were sitting in the park.
                nsubj(seen, Mary)
                cc(Mary, and)
                conj(Mary, John)
                -> return ['Mary, 'John']
        """
        d = NounPhraseRuleset.extract(self, relations, index, context, engine,
                                      info)
        return d


class NsubjpassRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'nsubjpass' relation."""

    rel = 'nsubjpass'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> list(str)
        OUTDATED

        This ruleset returns a list of strings, corresponding to the
            return_list value of NounPhraseRuleset.

        Examples:

            * The man was seen in the park.
                nsubjpass(seen, man)
                det(man, the)
                -> return ['the man']

            * Mary and John were seen in the park.
                nsubjpass(seen, Mary)
                cc(Mary, and)
                conj(Mary, John)
                -> return ['Mary, 'John']
        """
        d = NounPhraseRuleset.extract(self, relations, index, context, engine,
                                      info)
        return d


class DobjRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'dobj' relation."""

    rel = 'dobj'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> list(str)

        This ruleset returns a list of strings, corresponding to the
            return_list value of NounPhraseRuleset.

        Examples:

            * I saw her.
                dobj(saw, her)
                -> return ['her']

            * I saw Mary and John
                dobj(saw, Mary)
                cc(Mary, and)
                conj(Mary, John)
                -> return ['Mary, 'John']
        """
        d = NounPhraseRuleset.extract(self, relations, index, context, engine,
                                      info)
        if d['ids_for_preconj'] == []:
            return d['return_list']


class AdpobjRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'adpobj' relation."""

    rel = 'adpobj'


class IobjRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'iobj' relation."""

    rel = 'iobj'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> None

        The indirect object of a verb always generates a proposition.

        Examples:

            * I gave her a book.
                iobj(gave, her)
                -> emit(((to) her))
                -> return None

            * I gave John and Mary a book.
                iobj(gave, John)
                cc(John, and)
                conj(John, Mary)
                -> emit(((to) John))
                -> emit(((to) Mary))
                -> return None
        """
        d = NounPhraseRuleset.extract(self, relations, index, context,
                                      engine)
        if d['ids_for_preconj'] == []:
            for value in d['return_list']:
                engine.emit(('(DAT) ' + value,), 'M')


class PossRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'poss' relation."""

    rel = 'poss'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> str | None

        If the possessive modifier is a pronoun (PRP$), the pronoun is
            returned; if it's an NP modifier with a "'s", the NP is emitted
            as a proposition, and None is returned.

        Examples:

            * My friend
                poss(friend, My)
                -> return "My"

            * John's friend
                poss(friend, John)
                possessive(John, 's)
                -> emit((friend, John's))
                -> return None
        """
        # if relations[index].tag == 'PRP$':
        if relations[index].ctag == 'PRON':
            return relations[index].word
        # elif relations[index].tag in ('NN', 'NNS', 'NNP'):
        elif relations[index].ctag == 'NOUN':
            d = NounPhraseRuleset.extract(self, relations, index, context,
                                          engine)

            if d['ids_for_preconj'] == []:
                this = d['return_list']

                possessive_index = Relation.get_children_with_dep('adp',
                                                                  relations,
                                                                  index)[0]
                engine.analyze(relations, possessive_index, context + [index])

                referent = relations[context[-1]].word
                for item in this:
                    engine.emit((referent, item + "'s"), 'M')

                # TODO: handle multiple items.
                return None
        else:
            logger.warning('poss cannot handle %s yet', relations[index].ctag)


class TmodRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'tmod' relation."""

    rel = 'tmod'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> None

        A temporal modifier always generates a proposition.

        Examples:

            * Last night, I ran to the hills.
                tmod(ran, night)
                amod(night, Last)
                -> emit((Last night))
        """
        logger.warning('The "tmod" relation is not present in the Universal'
                       ' Dependencies, and is thus deprecated. It was replaced'
                       ' by nmod, advmod, amod, adpmod, or advcl, depending'
                       ' on the part of speech of the head word.')
        this = NounPhraseRuleset.extract(self, relations, index, context,
                                         engine, info)['return_list'][0]
        engine.emit((this, ), 'M')


class ApposRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'appos' relation."""

    rel = 'appos'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> None

        Appositional modifiers generate a special kind of predications.

        Examples:

            * John, my brother, was here.
                appos(John, brother)
                poss(brother, my)
                -> emit( ((APPOS), John, my brother) )
        """
        this = NounPhraseRuleset.extract(self, relations, index, context,
                                         engine, info)['return_list']
        for subj in info['subj']['return_list']:
            for noun in this:
                engine.emit(('(APPOS)', subj, noun), 'P')


class AttrRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'attr' relation."""

    rel = 'attr'
