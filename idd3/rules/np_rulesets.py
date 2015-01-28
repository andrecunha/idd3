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

import logging
logger = logging.getLogger(__name__)


class NounPhraseRuleset(Ruleset):

    """A base class for NP-like dependency substructures."""

    @staticmethod
    def process_determiners(relations, index, context, engine, info={}):

        """TODO: Docstring for process_determiners."""

        det_index = Relation.get_children_with_dep('det', relations, index)
        if det_index == []:
            det = None
        else:
            det = engine.analyze(relations, det_index[0], context + [index])

        return det

    @staticmethod
    def process_possessives(relations, index, context, engine, info={}):

        """TODO: Docstring for process_possessives."""

        poss_index = Relation.get_children_with_dep('poss', relations, index)
        if poss_index == []:
            poss = None
        else:
            poss = engine.analyze(relations, poss_index[0], context + [index])

        return poss

    @staticmethod
    def process_noun_modifiers(relations, index, context, engine, info={}):

        """TODO: Docstring for process_noun_modifiers."""

        nnjoin_indices = Relation.get_children_with_dep('nn-join', relations,
                                                        index)
        nns = [engine.analyze(relations, i, context + [index])
               for i in nnjoin_indices]

        return nns

    @staticmethod
    def process_conjs(relations, index, context, engine, info={}):

        """TODO: Docstring for process_conjs."""

        # Composite NP with conjunction

        cc_index = Relation.get_children_with_dep('cc', relations, index)
        if cc_index != []:
            engine.analyze(relations, cc_index[0], context + [index])
            conj_index = Relation.get_children_with_dep('conj', relations,
                                                        index)
            conjs = [engine.analyze(relations, i, context + [index],
                                    info={'class': 'NP'})
                     for i in conj_index]
            # TODO: check if this makes sense.
            conjs = [c[0] for c in conjs]
        else:
            conjs = []

        conjs = [relations[index].word] + conjs

        return conjs

    @staticmethod
    def process_preps(relations, index, context, engine, info={}):

        """TODO: Docstring for process_preps."""

        # VP modifiers
        prep_indices = Relation.get_children_with_dep('prep', relations, index)
        for i in prep_indices:
            engine.analyze(relations, i, context + [index])

    @staticmethod
    def process_modifiers(relations, index, context, engine, info={}):

        """TODO: Docstring for process_modifiers."""

        # ADJP modifiers
        amod_indices = Relation.get_children_with_dep('amod', relations, index)
        num_indices = Relation.get_children_with_dep('num', relations, index)
        nn_indices = Relation.get_children_with_dep('nn', relations, index)

        mods_indices = sorted(amod_indices + num_indices + nn_indices)
        mods = []
        for m in mods_indices:
            mod = engine.analyze(relations, m, context + [index])
            if isinstance(mod, str):
                mods.append(mod)
            elif isinstance(mod, list):
                mods += mod

        logger.debug('These are the modifiers: %s', mods)

        return mods

    @staticmethod
    def process_preconj(relations, index, context, engine, info={}):

        """TODO: Docstring for process_preconj."""

        preconj_indices = Relation.get_children_with_dep('preconj', relations,
                                                         index)
        if preconj_indices != []:
            preconj = engine.analyze(relations, preconj_indices[0],
                                     context + [index])
        else:
            preconj = None

        return preconj

    @staticmethod
    def process_vmod(relations, index, context, engine, info={}):

        """TODO: Docstring for process_vmod."""

        vmod_indices = Relation.get_children_with_dep('vmod', relations,
                                                      index)
        for i in vmod_indices:
            engine.analyze(relations, i, context + [index],
                           {'subj': {'return_list': ['NO_SUBJ'],
                                     'rcmod_wdt': None}})

    @staticmethod
    def process_rcmod(relations, index, context, engine, info={}):

        """TODO: Docstring for process_rcmod."""

        rcmod_indices = Relation.get_children_with_dep('rcmod', relations,
                                                       index)

        ids = []
        wdt = None
        for i in rcmod_indices:
            # _, ids, wdt = engine.analyze(relations, i, context + [index])
            ret = engine.analyze(relations, i, context + [index], info)
            ids = ret['prop_ids']
            wdt = ret['subjs']

        return ids, wdt

    @staticmethod
    def process_negs(relations, index, context, engine, info):

        """TODO: Docstring for process_negs."""

        # neg
        neg_indices = Relation.get_children_with_dep('neg', relations, index)
        for i in neg_indices:
            engine.analyze(relations, i, context + [index])

    @staticmethod
    def process_npadvmods(relations, index, context, engine, info):

        """TODO: Docstring for process_npadvmods."""

        npadvmod_indices = Relation.get_children_with_dep('npadvmod',
                                                          relations, index)
        for i in npadvmod_indices:
            mod = engine.analyze(relations, i, context + [index])
            engine.emit((mod,), 'M')

    @staticmethod
    def process_advmods(relations, index, context, engine, info):

        """TODO: Docstring for process_advmods."""

        advmod_indices = Relation.get_children_with_dep('advmod',
                                                        relations, index)
        for i in advmod_indices:
            engine.analyze(relations, i, context + [index])

    @staticmethod
    def process_appos(relations, index, context, engine, info):

        """TODO: Docstring for process_appos."""

        appos_indices = Relation.get_children_with_dep('appos',
                                                       relations, index)
        for i in appos_indices:
            engine.analyze(relations, i, context + [index], info)

    @staticmethod
    def assemble_return_list(det, poss, nns, conjs):

        """TODO: Docstring for assemble_return_list."""

        # TODO: properly handle distribution of possessives.
        return_list = []
        ids_for_preconj = []    # Ids of propositions for reference by eventual
        # preconj propositions.

        for conj in conjs:
            if nns != []:
                if isinstance(nns[0], str):
                    # Multiple nn modifying the same noun. Join to conj.
                    return_value = [word for word in [det, poss] + nns + [conj]
                                    if word is not None]
                    return_list.append(' '.join(return_value))
                elif isinstance(nns[0], list):
                    # Single nn with cc/conj. Emit different propositions.
                    for nn in nns[0]:
                        return_value = [word for word in [det, poss, nn, conj]
                                        if word is not None]
                        return_list.append(' '.join(return_value))
                        ids_for_preconj.append(len(return_list) - 1)

            else:
                # No nn.
                return_value = [word for word in [det, poss, conj]
                                if word is not None]
                return_list.append(' '.join(return_value))

        return return_list, ids_for_preconj

    def handle_np_with_of_phrase(relations, index, context, engine, info={}):

        """Handle noun phrases that start with 'of' phrases, such as
            'some of'."""

        prep_index = Relation.get_children_with_dep('prep', relations, index)[0]
        pobj_index = Relation.get_children_with_dep('pobj', relations,
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
                relations[relations[index].deps[0]].rel == 'prep':
            return NounPhraseRuleset.handle_np_with_of_phrase(relations, index,
                                                              context, engine,
                                                              info)

        det = NounPhraseRuleset.process_determiners(relations, index, context,
                                                    engine, info)

        poss = NounPhraseRuleset.process_possessives(relations, index, context,
                                                     engine, info)

        nns = NounPhraseRuleset.process_noun_modifiers(relations, index,
                                                       context, engine, info)

        conjs = NounPhraseRuleset.process_conjs(relations, index, context,
                                                engine, info)

        NounPhraseRuleset.process_preps(relations, index, context, engine, info)

        mods = NounPhraseRuleset.process_modifiers(relations, index,
                                                   context, engine, info)

        NounPhraseRuleset.process_vmod(relations, index, context, engine, info)

        NounPhraseRuleset.process_negs(relations, index, context, engine, info)

        NounPhraseRuleset.process_npadvmods(relations, index, context,
                                            engine, info)

        NounPhraseRuleset.process_advmods(relations, index, context,
                                          engine, info)

        return_list, ids_for_preconj = NounPhraseRuleset.\
            assemble_return_list(det, poss, nns, conjs)

        NounPhraseRuleset.process_appos(relations, index, context,
                                        engine,
                                        {'subj':
                                         {'return_list': return_list,
                                          'rcmod_wdt': None}})

        # Emit propositions for modifiers
        for amod in mods:
            for noun in return_list:
                engine.emit((noun, amod), 'M')

        preconj = NounPhraseRuleset.process_preconj(relations, index, context,
                                                    engine, info)

        ids, wdt = NounPhraseRuleset.process_rcmod(relations, index, context,
                                                   engine,
                                                   {'subj':
                                                    {'return_list': return_list,
                                                     'rcmod_wdt': None}})

        return {'return_list': return_list,
                'preconj': preconj,
                'ids_for_preconj': ids_for_preconj,
                'rcmod_wdt': wdt,
                'rcmod_ids': ids}


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


class PobjRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'pobj' relation."""

    rel = 'pobj'


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
                engine.emit(('(to) ' + value,), 'PREP')


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
        if relations[index].tag == 'PRP$':
            return relations[index].word
        elif relations[index].tag in ('NN', 'NNS', 'NNP'):
            d = NounPhraseRuleset.extract(self, relations, index, context,
                                          engine)

            if d['ids_for_preconj'] == []:
                this = d['return_list']

                possessive_index = Relation.get_children_with_dep('possessive',
                                                                  relations,
                                                                  index)[0]
                engine.analyze(relations, possessive_index, context + [index])

                referent = relations[context[-1]].word
                for item in this:
                    engine.emit((referent, item + "'s"), 'M')

                # TODO: handle multiple items.
                return None
        else:
            print('WARNING: poss cannot handle', relations[index].tag, 'yet')


class NpadvmodRuleset(Ruleset):

    """A ruleset that processes the 'npadvmod' relation."""

    rel = 'npadvmod'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> str

        This ruleset returns the NP modifier as a string, without emiting
            any proposition.

        Examples:

            * He is 40 years old.
                npadvmod(old, years)
                num(years, 40)
                -> return "40 years"
        """
        det_indices = Relation.get_children_with_dep('det', relations, index)
        poss_indices = Relation.get_children_with_dep('poss', relations, index)
        nn_indices = Relation.get_children_with_dep('nn', relations, index)
        prep_indices = Relation.get_children_with_dep('prep', relations, index)
        amod_indices = Relation.get_children_with_dep('amod', relations, index)
        num_indices = Relation.get_children_with_dep('num', relations, index)

        word_indices = sorted(det_indices + poss_indices + nn_indices +
                              prep_indices + amod_indices + num_indices +
                              [index])

        words = []
        for w in word_indices:
            if w == index:
                word = relations[index].word
            else:
                word = engine.analyze(relations, w, context + [index])

            if isinstance(word, str):
                words.append(word)
            elif isinstance(word, list):
                words += word

        return ' '.join(words)


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
        this = NounPhraseRuleset.extract(self, relations, index, context,
                                         engine, info)['return_list'][0]
        engine.emit((this, ), 'M')


class ApposRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'appos' relation."""

    rel = 'appos'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> None
        TODO
        """
        this = NounPhraseRuleset.extract(self, relations, index, context,
                                         engine, info)['return_list'][0]
        for subj in info['subj']:
            engine.emit(('(is)', subj, this), 'P')
