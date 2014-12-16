# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Ruleset


be_forms = ['am', 'are', 'is', 'being', 'was', 'were', 'been']


# Base classes.


class VerbPhraseRuleset(Ruleset):

    """A base class for VP-like dependency substructures."""

    @staticmethod
    def process_subj(relations, index, context, engine, info):

        """TODO: Docstring for process_subj."""

        # nsubj
        subj_index = Relation.get_children_with_dep('nsubj', relations, index)
        if subj_index == []:
            if 'subj' in info:
                subj = ['(%s)' % info['subj']]
            else:
                subj = ['(NO_SUBJ)']  # TODO: remove.
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
            subj = [engine.analyze(relations, subj_index[0], context + [index])]

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
            engine.emit((relations[index].word, mod))

    @staticmethod
    def process_pp_when_be_is_root(relations, index, context, engine, info,
                                   subjs):

        """TODO: Docstring for process_pp_when_be_is_root."""

        prep_indices = Relation.get_children_with_dep('prep', relations,
                                                      index)
        if prep_indices == []:
            return []

        if subjs[0].lower() == 'it':
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
            if subjs[0].lower() == 'it':
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
    def process_advcl(relations, index, context, engine, info):
        advcl_indices = Relation.get_children_with_dep('advcl',
                                                       relations, index)

        advcl_markers = [engine.analyze(relations, i, context + [index])
                         for i in advcl_indices]

        return advcl_markers

    def emit_propositions(self, verb, subjs, dobjs, engine, relation):

        """TODO: Docstring for emit_propositions."""

        if relation.tag == 'VBG' and relation.rel != 'null':
            for dobj in dobjs:
                proposition = tuple([w for w in [verb, dobj]])
                engine.emit(proposition)
        else:
            for subj in subjs:
                if len(dobjs) > 0:
                    for dobj in dobjs:
                        proposition = tuple([w for w in [verb, subj, dobj]])
                        engine.emit(proposition)
                else:
                    engine.emit((verb, subj))

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
        if mods != []:
            if subjs[0].lower() == 'it':
                # 'It' is usually considered a dummy, semantically empty
                #   subject, so we join the adverbial and prepositional
                #   modifiers (usually a date, an age, or something similar)
                #   in the main proposition.
                for subj in subjs:
                    for mod in mods:
                        engine.emit((verb, subj, mod))
            else:
                for subj in subjs:
                    engine.emit((verb, subj))
        else:
            for subj in subjs:
                engine.emit((verb, subj))

    def handle_action_verb(self, relations, index, context, engine, info):

        """Handle an action verb as the VP root."""

        subjs = self.process_subj(relations, index, context, engine, info)

        auxs = self.process_auxs(relations, index, context, engine, info)

        prt = self.process_prt(relations, index, context, engine, info)

        verb = ' '.join([word for word in auxs + [relations[index].word, prt]
                         if word is not None])

        comps = self.process_comps(relations, index, context, engine,
                                   {'subj': subjs[0]})  # TODO: change this.

        self.process_ccomp(relations, index, context, engine,
                           {'subj': subjs[0]})  # TODO: change this.

        self.process_iobj(relations, index, context, engine, info)

        self.process_advs(relations, index, context, engine, info)

        self.process_ignorables(relations, index, context, engine, info)

        # Emit propositions.
        if relations[index].rel in ('xcomp', 'ccomp', 'pcomp', 'csubj'):
            if relations[index].tag == 'VBG':
                if comps != []:
                    self.emit_propositions(verb, subjs, comps, engine,
                                           relations[index])
                return relations[index].word
            else:
                self.emit_propositions(verb, subjs, comps, engine,
                                       relations[index])
                return None
        else:
            self.emit_propositions(verb, subjs, comps, engine,
                                   relations[index])
            return None

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

        for subj in subjs:
            for compl in complms:
                # engine.emit((verb, subj, relations[index].word))
                engine.emit((verb, subj, compl))

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

        for subj in subjs:
            for word in this:
                engine.emit((verb, subj, word))

    def extract(self, relations, index, context, engine, info={}):
        # Process discourse markers.
        VerbPhraseRuleset.process_discourse_markers(relations, index, context,
                                                    engine, info)

        if relations[index].word in be_forms:
            return self.handle_be_as_root(relations, index, context, engine,
                                          info)
        if relations[index].tag in ('VBZ', 'VBD', 'VBN', 'VB', 'VBG', 'VBP'):
            return self.handle_action_verb(relations, index, context, engine,
                                           info)
        elif relations[index].tag in ('NN', 'NNS', 'NNP', 'NNPS', 'CD'):
            return self.handle_cop_with_np(relations, index, context, engine,
                                           info)
        elif relations[index].tag in ('JJ'):
            return self.handle_cop_with_adjp(relations, index, context, engine,
                                             info)
        else:
            print('VP: cannot handle', relations[index].tag, 'yet.')

        # Process adverbial clauses.
        VerbPhraseRuleset.process_advcl(relations, index, context, engine, info)


class AtomicRuleset(Ruleset):

    """A base ruleset for atomic relations that just returns the associated
    word."""

    def extract(self, relations, index, context, engine, info={}):
        return relations[index].word


class AtomicEmittingRuleset(Ruleset):

    """A base ruleset for atomic relations that just emits the associated word
    as a proposition."""

    def extract(self, relations, index, context, engine, info={}):
        engine.emit((relations[index].word,))


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

        nn_indices = Relation.get_children_with_dep('nn', relations, index)
        nns = [engine.analyze(relations, i, context + [index])
               for i in nn_indices]

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
            conjs = [engine.analyze(relations, i, context + [index])
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
        prep_index = Relation.get_children_with_dep('prep', relations, index)
        if prep_index != []:
            engine.analyze(relations, prep_index[0], context + [index])

    @staticmethod
    def process_modifiers(relations, index, context, engine, info={}):

        """TODO: Docstring for process_modifiers."""

        # ADJP modifiers
        amod_indices = Relation.get_children_with_dep('amod', relations, index)
        num_indices = Relation.get_children_with_dep('num', relations, index)

        mods_indices = sorted(amod_indices + num_indices)
        mods = []
        for m in mods_indices:
            mod = engine.analyze(relations, m, context + [index])
            if isinstance(mod, str):
                mods.append(mod)
            elif isinstance(mod, list):
                mods += mod

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
            engine.analyze(relations, i, context + [index], {'subj': 'NO_SUBJ'})

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
                         relations[prep_index].word))

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

        return_list, ids_for_preconj = NounPhraseRuleset.\
            assemble_return_list(det, poss, nns, conjs)

        # Emit propositions for modifiers
        for amod in mods:
            for noun in return_list:
                engine.emit((noun, amod))

        preconj = NounPhraseRuleset.process_preconj(relations, index, context,
                                                    engine, info)

        return {'return_list': return_list,
                'preconj': preconj,
                'ids_for_preconj': ids_for_preconj}


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


# Derived classes.


class TopRuleset(Ruleset):

    """A dummy ruleset that starts the analysis process."""

    rel = 'TOP'

    def extract(self, relations, index, context, engine, info={}):
        return engine.analyze(relations, relations[index].deps[0], [index])


# Verb-Phrase rulesets.


class RootRuleset(VerbPhraseRuleset):

    """A ruleset that processes the 'ROOT' relation."""

    rel = 'null'


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


# Atomic rulesets.


class PrtRuleset(AtomicRuleset):

    """A ruleset that processes the 'prt' relation."""

    rel = 'prt'


class AuxRuleset(AtomicRuleset):

    """A ruleset that processes the 'aux' relation."""

    rel = 'aux'


class AuxpassRuleset(AtomicRuleset):

    """A ruleset that processes the 'auxpass' relation."""

    rel = 'auxpass'


class CcRuleset(AtomicRuleset):

    """A ruleset that processes the 'cc' relation."""

    rel = 'cc'


class CopRuleset(AtomicRuleset):

    """A ruleset that processes the 'cop' relation."""

    rel = 'cop'


class ComplmRuleset(AtomicRuleset):

    """A ruleset that processes the 'complm' relation."""

    rel = 'complm'


class PossessiveRuleset(AtomicRuleset):

    """A ruleset that processes the 'possessive' relation."""

    rel = 'possessive'


class NumberRuleset(AtomicRuleset):

    """A ruleset that processes the 'number' relation."""

    rel = 'number'


class PreconjRuleset(AtomicRuleset):

    """A ruleset that processes the 'preconj' relation."""

    rel = 'preconj'


# Atomic emitting rulesets.


class NegRuleset(AtomicEmittingRuleset):

    """A ruleset that processes the 'neg' relation."""

    rel = 'neg'


class DiscourseRuleset(AtomicEmittingRuleset):

    """A ruleset that processes the 'discourse' relation."""

    rel = 'discourse'


# Noun-Phrase rulesets.


class NsubjRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'nsubj' relation."""

    rel = 'nsubj'

    def extract(self, relations, index, context, engine, info={}):
    	"""extract(relations, index, context, engine, info) -> list(str)

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
        if d['ids_for_preconj'] == []:
            return d['return_list']


class NsubjpassRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'nsubjpass' relation."""

    rel = 'nsubjpass'

    def extract(self, relations, index, context, engine, info={}):
    	"""extract(relations, index, context, engine, info) -> list(str)

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
        if d['ids_for_preconj'] == []:
            return d['return_list']


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
                engine.emit(('(to) ' + value,))


class ConjRuleset(NounPhraseRuleset):

    """A ruleset that processes the 'conj' relation."""

    rel = 'conj'

    def extract(self, relations, index, context, engine, info={}):
    	"""extract(relations, index, context, engine, info) -> list(str)

    	This ruleset returns a list of strings, corresponding to the
    		return_list value of NounPhraseRuleset.

    	Examples:

    		* Mary and John
    			conj(Mary, John)
    			-> return ['John']
    	"""
    	# TODO: Maybe just return the first element in the list.
        d = NounPhraseRuleset.extract(self, relations, index, context,
                                      engine)
        if d['ids_for_preconj'] == []:
            return d['return_list']


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
                    engine.emit((referent, item + "'s"))

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
        engine.emit((this, ))


# Adjectival-Phrase rulesets


class AcompRuleset(AdjectivalPhraseRuleset):

    """A ruleset that processes the 'acomp' relation."""

    rel = 'acomp'


class AmodRuleset(AdjectivalPhraseRuleset):

    """A ruleset that processes the 'amod' relation."""

    rel = 'amod'


# Adverbial-Phrase rulesets


class AdvmodRuleset(AdverbialPhraseRuleset):

    """A ruleset that processes the 'advmod' relation."""

    rel = 'advmod'


# Uncategorized rulesets.


class NnRuleset(Ruleset):

    """A ruleset that processes the 'nn' relation."""

    rel = 'nn'

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
        cc_indices = Relation.get_children_with_dep('cc', relations, index)

        if cc_indices != []:
            engine.analyze(relations, cc_indices[0], context + [index])
            conj_indices = Relation.get_children_with_dep('conj', relations,
                                                          index)
            conjs = [engine.analyze(relations, i, context + [index])
                     for i in conj_indices]
            conjs = [c[0] for c in conjs]  # TODO: check if this makes sense.

            return [relations[index].word] + conjs
        else:
            return relations[index].word


class DetRuleset(Ruleset):

    """A ruleset that processes the 'det' relation."""

    rel = 'det'

    non_emitted_dets = ('the', 'a', 'an', 'this', 'these')

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
            engine.emit((relations[context[-1]].word, relations[index].word))
            return None


class PrepRuleset(Ruleset):

    """A ruleset that processes the 'prep' relation."""

    rel = 'prep'

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
        # pobj
        pobj_index = Relation.get_children_with_dep('pobj', relations, index)
        if pobj_index != []:
            pobjs = engine.analyze(relations, pobj_index[0], context + [index])

            emitted_prop_ids = []
            for pobj in pobjs['return_list']:
                prop_id = engine.emit((relations[index].word + ' ' + pobj,))
                emitted_prop_ids.append(prop_id)

            if pobjs['ids_for_preconj'] != []:
                indices = [j for i, j in enumerate(emitted_prop_ids)
                           if i in pobjs['ids_for_preconj']]
                proposition = tuple([pobjs['preconj']] + indices)
                engine.emit(proposition)

        # pcomp
        pcomp_index = Relation.get_children_with_dep('pcomp', relations, index)
        if pcomp_index != []:
            pcomp = engine.analyze(relations, pcomp_index[0],
                                   context + [index])
            if pcomp is not None:
                engine.emit((relations[index].word + ' ' + pcomp,))
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
        number_indices = Relation.get_children_with_dep('number',
                                                        relations, index)
        cc_indices = Relation.get_children_with_dep('cc',
                                                    relations, index)
        conj_indices = Relation.get_children_with_dep('conj',
                                                      relations, index)

        indices = sorted([index] + number_indices + cc_indices + conj_indices)

        words = []
        for n in indices:
            if n != index:
                word = engine.analyze(relations, n, context + [index])
            else:
                word = relations[index].word

            if isinstance(word, str):
                words.append(word)
            elif isinstance(word, list):
                words += word

        this_number = ' '.join(words)

        # Process quantmods
        quantmod_indices = Relation.get_children_with_dep('quantmod',
                                                          relations, index)
        for q in quantmod_indices:
            engine.analyze(relations, q, context + [index],
                           {'num': this_number})

        return this_number


class QuantmodRuleset(Ruleset):

    """A ruleset that processes the 'quantmod' relation."""

    rel = 'quantmod'

    def extract(self, relations, index, context, engine, info):
        """extract(relations, index, context, engine, info) -> None

        Quantifier phrase modifiers always generate propositions.

        Examples:

            * About 100
                quantmod(100, about)
                -> emit((100, about))
        """
        engine.emit((info['num'], relations[index].word))


all_rulesets = [TopRuleset(),
                # Verb-Phrase rulesets.
                RootRuleset(),
                XcompRuleset(),
                CcompRuleset(),
                PcompRuleset(),
                CsubjRuleset(),
                VmodRuleset(),
                AdvclRuleset(),
                # Atomic rulesets.
                PrtRuleset(),
                AuxRuleset(),
                AuxpassRuleset(),
                CcRuleset(),
                CopRuleset(),
                ComplmRuleset(),
                PossessiveRuleset(),
                NumberRuleset(),
                PreconjRuleset(),
                # Atomic emitting rulesets.
                NegRuleset(),
                DiscourseRuleset(),
                # Noun-Phrase rulesets.
                NsubjRuleset(),
                NsubjpassRuleset(),
                DobjRuleset(),
                PobjRuleset(),
                IobjRuleset(),
                ConjRuleset(),
                PossRuleset(),
                NpadvmodRuleset(),
                TmodRuleset(),
                # Adjectival-Phrase rulesets
                AcompRuleset(),
                AmodRuleset(),
                # Adverbial-Phrase rulesets
                AdvmodRuleset(),
                # Uncategorized rulesets.
                NnRuleset(),
                DetRuleset(),
                PrepRuleset(),
                QuantmodRuleset(),
                NumRuleset()]
