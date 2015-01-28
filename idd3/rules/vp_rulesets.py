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
from idd3.rules.adjp_rulesets import AdjectivalPhraseRuleset
from idd3.rules.np_rulesets import NounPhraseRuleset
import logging


logger = logging.getLogger(__name__)

be_forms = ['am', 'are', 'is', 'being', 'was', 'were', 'been']


class VerbPhraseRuleset(Ruleset):

    """A base class for VP-like dependency substructures."""

    @staticmethod
    def process_subj(relations, index, context, engine, info):

        """TODO: Docstring for process_subj."""

        # nsubj
        subj_index = Relation.get_children_with_dep('nsubj', relations, index)
        if subj_index == []:
            if 'subj' in info:
                subj = {'return_list': ['(%s)' % s
                                        for s in info['subj']['return_list']],
                        'rcmod_wdt': None}
            else:
                subj = {'return_list': ['(NO_SUBJ)'], 'rcmod_wdt': None}
                # TODO: remove.
        else:
            subj = engine.analyze(relations, subj_index[0], context + [index])

        # nsubjpass
        subj_index = Relation.get_children_with_dep('nsubjpass', relations,
                                                    index)
        if subj_index != []:
            subj = engine.analyze(relations, subj_index[0], context + [index])

        # csubj
        subj_index = Relation.get_children_with_dep('csubj', relations, index)
        if subj_index != []:
            subj = {'return_list': [engine.analyze(relations, subj_index[0],
                                                   context + [index])
                                    ['return_value']],
                    'rcmod_wdt': None}

        # Resolve relative pronouns in subordinate clauses.
        if subj['return_list'][0] in ('that', 'which', 'who')\
                and 'subj' in info:
            subj['return_list'][0] += '(={0})'.format(
                info['subj']['return_list'][0])

        return subj

    @staticmethod
    def process_auxs(relations, index, context, engine, info):

        """TODO: Docstring for process_auxs."""

        # TODO: add support for multiple auxiliaries.
        aux_index = Relation.get_children_with_dep('aux', relations, index)
        auxpass_index = Relation.get_children_with_dep('auxpass', relations,
                                                       index)
        auxs_index = sorted(aux_index + auxpass_index)
        auxs = [engine.analyze(relations, i, context + [index])
                for i in auxs_index]

        if auxs == [] and 'aux' in info:
            auxs = info['aux']

        return auxs

    @staticmethod
    def process_prt(relations, index, context, engine, info):

        """TODO: Docstring for process_prt."""

        prt_index = Relation.get_children_with_dep('prt', relations, index)
        if prt_index == []:
            prt = None
        else:
            prt = engine.analyze(relations, prt_index[0], context + [index])

        return prt

    @staticmethod
    def process_comps(relations, index, context, engine, info):

        """TODO: Docstring for process_comps."""

        dobj_index = Relation.get_children_with_dep('dobj', relations, index)
        xcomp_index = Relation.get_children_with_dep('xcomp', relations, index)
        acomp_index = Relation.get_children_with_dep('acomp', relations, index)

        comps_indices = sorted(dobj_index + xcomp_index + acomp_index)
        _comps = [engine.analyze(relations, i, context + [index], info)
                  for i in comps_indices]

        comps = []
        for comp in _comps:
            if isinstance(comp, dict):
                comp = comp['return_value']

            if isinstance(comp, list):
                comps.extend(comp)
            else:
                if comp is not None:
                    comps.append(comp)

        return comps

    @staticmethod
    def process_ccomp(relations, index, context, engine, info):

        """TODO: Docstring for process_ccomp."""

        ccomp_index = Relation.get_children_with_dep('ccomp', relations, index)
        if ccomp_index != []:
            engine.analyze(relations, ccomp_index[0], context + [index], info)

    @staticmethod
    def process_iobj(relations, index, context, engine, info):

        """TODO: Docstring for process_iobj."""

        # prep + pobj
        prep_indices = Relation.get_children_with_dep('prep', relations, index)
        for prep_index in prep_indices:
            engine.analyze(relations, prep_index, context + [index])

        # iobj
        iobj_index = Relation.get_children_with_dep('iobj', relations, index)
        if iobj_index != []:
            engine.analyze(relations, iobj_index[0], context + [index])

    @staticmethod
    def process_advs(relations, index, context, engine, info):

        """TODO: Docstring for process_advs."""

        # advmod
        advmod_indices = Relation.get_children_with_dep('advmod', relations,
                                                        index)
        for i in advmod_indices:
            engine.analyze(relations, i, context + [index])

        # tmod
        tmod_indices = Relation.get_children_with_dep('tmod', relations, index)
        for i in tmod_indices:
            engine.analyze(relations, i, context + [index])

        # neg
        neg_indices = Relation.get_children_with_dep('neg', relations, index)
        for i in neg_indices:
            engine.analyze(relations, i, context + [index])

    @staticmethod
    def process_ignorables(relations, index, context, engine, info):

        """TODO: Docstring for process_ignorables."""

        # complm
        complm_indices = Relation.get_children_with_dep('complm', relations,
                                                        index)
        for i in complm_indices:
            engine.analyze(relations, i, context + [index])

    @staticmethod
    def process_npadvmod(relations, index, context, engine, info):

        """TODO: Docstring for process_npadvmod."""

        # npadvmod
        npadvmod_indices = Relation.get_children_with_dep('npadvmod',
                                                          relations,
                                                          index)
        mods = [engine.analyze(relations, i, context + [index])
                for i in npadvmod_indices]

        for mod in mods:
            engine.emit((relations[index].word, mod), 'M')

    @staticmethod
    def process_pp_when_be_is_root(relations, index, context, engine, info,
                                   subjs):

        """TODO: Docstring for process_pp_when_be_is_root."""

        prep_indices = Relation.get_children_with_dep('prep', relations,
                                                      index)
        if prep_indices == []:
            return []

        if subjs['return_list'][0].lower() == 'it':
            prep_index = prep_indices[0]
            pobj_index = Relation.get_children_with_dep('pobj', relations,
                                                        prep_index)[0]

            pobj_return_value = engine.analyze(relations, pobj_index, context +
                                               [index, prep_index])

            return_list = []
            for noun in pobj_return_value['return_list']:
                return_list.append(relations[prep_index].word + ' ' + noun)

            engine.mark_processed(relations, prep_index)

            return return_list
        else:
            for prep_index in prep_indices:
                engine.analyze(relations, prep_index, context + [index])
            return []

    @staticmethod
    def process_advmod_when_be_is_root(relations, index, context, engine, info,
                                       subjs):

        """TODO: Docstring for process_advmod_when_be_is_root."""

        advmod_indices = Relation.get_children_with_dep('advmod', relations,
                                                        index)
        if advmod_indices != []:
            if subjs['return_list'][0].lower() == 'it':
                _info = {'no_emit': True}
            else:
                _info = {}

            advmod = [engine.analyze(relations, advmod_indices[0],
                                     context + [index], _info)]
        else:
            advmod = []

        return advmod

    @staticmethod
    def process_discourse_markers(relations, index, context, engine, info):

        """TODO: Docstring for process_discourse_markers."""

        discourse_indices = Relation.get_children_with_dep('discourse',
                                                           relations, index)

        for i in discourse_indices:
            engine.analyze(relations, i, context + [index])

    @staticmethod
    def process_advcl(relations, index, context, engine, info, prop_ids):
        advcl_indices = Relation.get_children_with_dep('advcl',
                                                       relations, index)

        for i in advcl_indices:
            ret = engine.analyze(relations, i, context + [index])
            for p in prop_ids:
                prop = tuple([ret['marker'], p] + ret['prop_ids'])
                engine.emit(prop, 'C')

    @staticmethod
    def process_conjs(relations, index, context, engine, info, subjs, auxs,
                      prop_ids):
        conj_indices = Relation.get_children_with_dep('conj', relations,
                                                      index)

        if conj_indices != []:
            cc_indices = Relation.get_children_with_dep('cc', relations, index)

            if cc_indices:
                conjunction = engine.analyze(relations, cc_indices[0],
                                             context + [index])
            else:
                conjunction = None

            preconj_indices = Relation.get_children_with_dep('preconj',
                                                             relations, index)
            if preconj_indices != []:
                preconj = engine.analyze(relations, preconj_indices[0],
                                         context + [index])
                conjunction = preconj + '_' + conjunction

            for i in conj_indices:
                ret = engine.analyze(relations, i, context + [index],
                                     info={'class': 'VP',
                                           'subj': subjs,
                                           'aux': auxs})
                prop_ids.extend(ret['prop_ids'])

            if conjunction:
                conj_prop = tuple([conjunction] + prop_ids)
                engine.emit(conj_prop, 'C')

    @staticmethod
    def process_parataxes(relations, index, context, engine, info):
        parataxis_indices = Relation.get_children_with_dep('parataxis',
                                                           relations, index)

        for i in parataxis_indices:
            engine.analyze(relations, i, context + [index])

    @staticmethod
    def process_whats(relations, index, context, engine, info):

        """Processes children with label 'what'."""

        what_indices = Relation.get_children_with_dep('what', relations, index)

        for i in what_indices:
            engine.analyze(relations, i, context + [index], info)

    def emit_propositions(self, verb, subjs, dobjs, engine, relation):

        """TODO: Docstring for emit_propositions."""

        prop_ids = []

        if relation.tag == 'VBG' and relation.rel not in ('null', 'root',
                                                          'conj'):
            for dobj in dobjs:
                    proposition = tuple([w for w in [verb, dobj]])
                    prop_id = engine.emit(proposition, 'P')
                    prop_ids.append(prop_id)
        else:
            for subj in subjs['return_list']:
                if len(dobjs) > 0:
                    for dobj in dobjs:
                        proposition = tuple([w for w in [verb, subj, dobj]])
                        prop_id = engine.emit(proposition, 'P')
                        prop_ids.append(prop_id)
                else:
                    prop_id = engine.emit((verb, subj), 'P')
                    prop_ids.append(prop_id)

        return prop_ids

    @staticmethod
    def emit_propositions_rcmods(return_dict, engine):

        """Emits propositions for rcmods."""

        if return_dict['subjs']['rcmod_wdt']:
            for main_prop_id in return_dict['prop_ids']:
                for rcmod_prop_id in return_dict['subjs']['rcmod_ids']:
                    engine.emit(
                        (return_dict['subjs']['rcmod_wdt']['return_list'][0],
                         main_prop_id,
                         rcmod_prop_id),
                        'C')

        if 'this' in return_dict:
            # Emit propositions for copula + NP.
            for main_prop_id in return_dict['prop_ids']:
                for rcmod_prop_id in return_dict['this']['rcmod_ids']:
                    engine.emit(
                        (return_dict['this']['rcmod_wdt']['return_list'][0],
                         main_prop_id,
                         rcmod_prop_id),
                        'C')

    def handle_be_as_root(self, relations, index, context, engine, info):

        """Handle 'to be' as the VP root."""

        subjs = self.process_subj(relations, index, context, engine, info)

        auxs = self.process_auxs(relations, index, context, engine, info)

        verb = ' '.join([word for word in auxs + [relations[index].word]
                         if word is not None])

        # Prepositional modifiers.
        prep_mods = VerbPhraseRuleset.process_pp_when_be_is_root(relations,
                                                                 index, context,
                                                                 engine, info,
                                                                 subjs)

        # Adverbial modifiers.
        advmods = VerbPhraseRuleset.process_advmod_when_be_is_root(relations,
                                                                   index,
                                                                   context,
                                                                   engine, info,
                                                                   subjs)

        mods = prep_mods + advmods

        self.process_ignorables(relations, index, context, engine, info)

        # Emit propositions.
        prop_ids = []
        if mods != []:
            if subjs['return_list'][0].lower() == 'it':
                # 'It' is usually considered a dummy, semantically empty
                #   subject, so we join the adverbial and prepositional
                #   modifiers (usually a date, an age, or something similar)
                #   in the main proposition.
                for subj in subjs['return_list']:
                    for mod in mods:
                        prop_id = engine.emit((verb, subj, mod), 'P')
                        prop_ids.append(prop_id)
            else:
                for subj in subjs['return_list']:
                    prop_id = engine.emit((verb, subj), 'P')
                    prop_ids.append(prop_id)
        else:
            for subj in subjs['return_list']:
                prop_id = engine.emit((verb, subj), 'P')
                prop_ids.append(prop_id)

        self.subjs = subjs
        self.auxs = auxs

        return {'return_value': None, 'prop_ids': prop_ids}

    def handle_action_verb(self, relations, index, context, engine, info):

        """Handle an action verb as the VP root."""

        subjs = self.process_subj(relations, index, context, engine, info)

        auxs = self.process_auxs(relations, index, context, engine, info)

        prt = self.process_prt(relations, index, context, engine, info)

        verb = ' '.join([word for word in auxs + [relations[index].word, prt]
                         if word is not None])

        comps = self.process_comps(relations, index, context, engine,
                                   {'subj': subjs})

        self.process_ccomp(relations, index, context, engine,
                           {'subj': subjs})

        self.process_iobj(relations, index, context, engine, info)

        self.process_advs(relations, index, context, engine, info)

        self.process_ignorables(relations, index, context, engine, info)

        self.process_whats(relations, index, context, engine, {})

        self.subjs = subjs
        self.auxs = auxs

        # Emit propositions.
        prop_ids = []
        if relations[index].rel in ('xcomp', 'ccomp', 'pcomp', 'csubj'):
            if relations[index].tag == 'VBG':
                if comps != []:
                    prop_ids = self.emit_propositions(verb, subjs, comps,
                                                      engine, relations[index])
                return {'return_value': relations[index].word,
                        'prop_ids': prop_ids}
            else:
                prop_ids = self.emit_propositions(verb, subjs, comps, engine,
                                                  relations[index])
                return {'return_value': None, 'prop_ids': prop_ids}
        else:
            prop_ids = self.emit_propositions(verb, subjs, comps, engine,
                                              relations[index])
            return {'return_value': None, 'prop_ids': prop_ids}

    def handle_cop_with_np(self, relations, index, context, engine, info):

        """Handle copular verbs with NP complements."""

        subjs = self.process_subj(relations, index, context, engine, info)

        cop_index = Relation.get_children_with_dep('cop', relations, index)[0]
        cop = engine.analyze(relations, cop_index, context + [index])

        auxs = self.process_auxs(relations, index, context, engine, info)

        verb = ' '.join([word for word in auxs + [cop] if word is not None])

        self.process_ignorables(relations, index, context, engine, info)

        this = NounPhraseRuleset.extract(self, relations, index, context,
                                         engine, info)

        # TODO: handle cc/conj and preconj.
        complms = this['return_list']

        prop_ids = []
        for subj in subjs['return_list']:
            for compl in complms:
                # engine.emit((verb, subj, relations[index].word))
                prop_id = engine.emit((verb, subj, compl), 'P')
                prop_ids.append(prop_id)

        self.subjs = subjs
        self.auxs = auxs

        return {'return_value': None, 'prop_ids': prop_ids, 'this': this}

    def handle_cop_with_adjp(self, relations, index, context, engine, info):

        """Handle copular verbs with ADJP complements."""

        subjs = self.process_subj(relations, index, context, engine, info)

        cop_index = Relation.get_children_with_dep('cop', relations, index)[0]
        cop = engine.analyze(relations, cop_index, context + [index])

        auxs = self.process_auxs(relations, index, context, engine, info)

        verb = ' '.join([word for word in auxs + [cop] if word is not None])

        self.process_ignorables(relations, index, context, engine, info)

        self.process_npadvmod(relations, index, context, engine, info)

        this = AdjectivalPhraseRuleset.extract(self, relations, index, context,
                                               engine, info)

        prop_ids = []
        for subj in subjs['return_list']:
            for word in this:
                prop_id = engine.emit((verb, subj, word), 'P')
                prop_ids.append(prop_id)

        self.subjs = subjs
        self.auxs = auxs

        return {'return_value': None, 'prop_ids': prop_ids}

    def extract(self, relations, index, context, engine, info={}):
        # Process discourse markers.
        VerbPhraseRuleset.process_discourse_markers(relations, index, context,
                                                    engine, info)

        if relations[index].word in be_forms:
            return_dict = self.handle_be_as_root(relations, index, context,
                                                 engine, info)
        elif relations[index].tag in ('VBZ', 'VBD', 'VBN', 'VB', 'VBG', 'VBP'):
            return_dict = self.handle_action_verb(relations, index, context,
                                                  engine, info)
        elif relations[index].tag in ('NN', 'NNS', 'NNP', 'NNPS', 'CD', 'WP'):
            return_dict = self.handle_cop_with_np(relations, index, context,
                                                  engine, info)
        elif relations[index].tag in ('JJ'):
            return_dict = self.handle_cop_with_adjp(relations, index, context,
                                                    engine, info)
        else:
            print('VP: cannot handle', relations[index].tag, 'yet.')
            return_dict = None

        # Process adverbial clauses.
        VerbPhraseRuleset.process_advcl(relations, index, context, engine,
                                        info, return_dict['prop_ids'])

        # Process conjunctions.
        VerbPhraseRuleset.process_conjs(relations, index, context, engine,
                                        info, self.subjs, self.auxs,
                                        return_dict['prop_ids'])

        # Process parataxical clauses.
        VerbPhraseRuleset.process_parataxes(relations, index, context, engine,
                                            info)

        return_dict['subjs'] = self.subjs

        # Process rcmods.
        VerbPhraseRuleset.emit_propositions_rcmods(return_dict, engine)

        return return_dict


class RootRuleset(VerbPhraseRuleset):

    """A ruleset that processes the 'ROOT' relation."""

    rel = 'root'


class XcompRuleset(VerbPhraseRuleset):

    """A ruleset that processes the 'xcomp' relation."""

    rel = 'xcomp'


class CcompRuleset(VerbPhraseRuleset):

    """A ruleset that processes the 'ccomp' relation."""

    rel = 'ccomp'


class PcompRuleset(VerbPhraseRuleset):

    """A ruleset that processes the 'pcomp' relation."""

    rel = 'pcomp'


class CsubjRuleset(VerbPhraseRuleset):

    """A ruleset that processes the 'csubj' relation."""

    rel = 'csubj'


class VmodRuleset(VerbPhraseRuleset):

    """A ruleset that processes the 'vmod' relation."""

    rel = 'vmod'


class AdvclRuleset(VerbPhraseRuleset):

    """A ruleset that processes the 'advcl' relation."""

    rel = 'advcl'

    def extract(self, relations, index, context, engine, info={}):
        ret = VerbPhraseRuleset.extract(self, relations, index, context,
                                        engine, info)

        mark_index = Relation.get_children_with_dep('mark', relations, index)

        if mark_index != []:
            marker = engine.analyze(relations, mark_index[0], context + [index])
        else:
            marker = 'NO_MARKER'

        ret['marker'] = marker

        return ret
        # return status, prop_ids, marker


class RcmodRuleset(VerbPhraseRuleset):

    """A ruleset that processes the 'rcmod' relation."""

    rel = 'rcmod'


class ParataxisRuleset(VerbPhraseRuleset):

    """A ruleset that processes the 'parataxis' relation."""

    rel = 'parataxis'
