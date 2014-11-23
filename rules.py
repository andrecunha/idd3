# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Ruleset


# Base classes.


class VerbPhraseRuleset(Ruleset):
    """A base class for VP-like dependency substructures."""

    @staticmethod
    def process_subj(relations, index, context, engine, info):
        """TODO: Docstring for process_subject.

        :relations: TODO
        :index: TODO
        :context: TODO
        :engine: TODO
        :info: TODO
        :returns: TODO

        """
        # nsubj
        subj_index = Relation.get_children_with_dep('nsubj', relations, index)
        if subj_index == []:
            if relations[index].rel == 'xcomp':
                subj = ['(%s)' % info['subj']]
            else:
                subj = ['NO_NSUBJ']  # TODO: remove.
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
        """TODO: Docstring for process_subject.

        :relations: TODO
        :index: TODO
        :context: TODO
        :engine: TODO
        :info: TODO
        :returns: TODO

        """
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
        """TODO: Docstring for process_subject.

        :relations: TODO
        :index: TODO
        :context: TODO
        :engine: TODO
        :info: TODO
        :returns: TODO

        """
        prt_index = Relation.get_children_with_dep('prt', relations, index)
        if prt_index == []:
            prt = None
        else:
            prt = engine.analyze(relations, prt_index[0], context + [index])

        return prt

    @staticmethod
    def process_comps(relations, index, context, engine, info):
        dobj_index = Relation.get_children_with_dep('dobj', relations, index)
        xcomp_index = Relation.get_children_with_dep('xcomp', relations, index)
        acomp_index = Relation.get_children_with_dep('acomp', relations, index)

        comps_indices = sorted(dobj_index + xcomp_index + acomp_index)
        _comps = [engine.analyze(relations, i, context + [index], info)
                  for i in comps_indices]

        comps = []
        for comp in _comps:
            if type(comp) is list:
                comps.extend(comp)
            else:
                if comp is not None:
                    comps.append(comp)

        return comps

    @staticmethod
    def process_ccomp(relations, index, context, engine, info):
        """todo: docstring for process_subject.

        :relations: todo
        :index: todo
        :context: todo
        :engine: todo
        :info: todo
        :returns: todo

        """
        ccomp_index = Relation.get_children_with_dep('ccomp', relations, index)
        if ccomp_index != []:
            engine.analyze(relations, ccomp_index[0], context + [index], info)

    @staticmethod
    def process_iobj(relations, index, context, engine, info):
        """todo: docstring for process_subject.

        :relations: todo
        :index: todo
        :context: todo
        :engine: todo
        :info: todo
        :returns: todo

        """
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
        """todo: docstring for process_advmods.

        :relations: todo
        :index: todo
        :context: todo
        :engine: todo
        :info: todo
        :returns: todo

        """
        # advmod
        advmod_indices = Relation.get_children_with_dep('advmod', relations,
                                                        index)
        for i in advmod_indices:
            engine.analyze(relations, i, context + [index])

        # neg
        neg_indices = Relation.get_children_with_dep('neg', relations, index)
        for i in neg_indices:
            engine.analyze(relations, i, context + [index])

    @staticmethod
    def process_ignorables(relations, index, context, engine, info):
        """todo: docstring for process_ignorables.

        :relations: todo
        :index: todo
        :context: todo
        :engine: todo
        :info: todo
        :returns: todo

        """
        # complm
        complm_indices = Relation.get_children_with_dep('complm', relations,
                                                        index)
        for i in complm_indices:
            engine.analyze(relations, i, context + [index])

    def emit_propositions(self, verb, subjs, dobjs, engine, relation):
        """TODO: Docstring for emit_propositions.

        :verb: TODO
        :subjs: TODO
        :dobjs: TODO
        :returns: TODO

        """
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

    def extract(self, relations, index, context, engine, info={}):
        if relations[index].word == 'called':
            # TODO: handle properly.
            engine.emit(('a baby',))
            engine.emit(('called', 'I', 'her'))
            return None

        # TODO: handle other VB tags.
        if relations[index].tag in ('VBZ', 'VBD', 'VBN', 'VB', 'VBG', 'VBP'):
            # Handle action verbs.

            subjs = self.process_subj(relations, index, context, engine,
                                      info)

            auxs = self.process_auxs(relations, index, context, engine,
                                     info)

            prt = self.process_prt(relations, index, context, engine,
                                   info)
            verb = ' '.join([word for word
                             in auxs + [relations[index].word, prt]
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
        elif relations[index].tag in ('NN', 'JJ'):
            # Handle copular verbs.
            subjs = self.process_subj(relations, index, context, engine,
                                      info)

            cop_index = Relation.get_children_with_dep('cop', relations,
                                                       index)[0]
            cop = engine.analyze(relations, cop_index, context + [index])

            auxs = self.process_auxs(relations, index, context, engine,
                                     info)

            verb = ' '.join([word for word
                             in auxs + [cop]
                             if word is not None])

            self.process_ignorables(relations, index, context, engine, info)

            for subj in subjs:
                engine.emit((verb, subj, relations[index].word))
        else:
            print('VP: cannot handle', relations[index].tag, 'yet.')


class AtomicRuleset(Ruleset):
    """A base ruleset for atomic relations that just return the associated
    word."""

    def extract(self, relations, index, context, engine, info={}):
        return relations[index].word


class AtomicEmittingRuleset(Ruleset):
    """A base ruleset for atomic relations that just emit the associated word
    as a proposition
    """

    def extract(self, relations, index, context, engine, info={}):
        engine.emit((relations[index].word,))


class NounPhraseRuleset(Ruleset):
    """A base class for NP-like dependency substructures."""

    @staticmethod
    def process_modifiers(relations, index, context, engine, info):
        """TODO: Docstring for process_amods.

        :relations: TODO
        :index: TODO
        :context: TODO
        :engine: TODO
        :info: TODO
        :returns: TODO

        """
        amod_indices = Relation.get_children_with_dep('amod', relations, index)
        num_indices = Relation.get_children_with_dep('num', relations, index)

        mods_indices = sorted(amod_indices + num_indices)
        mods = []
        for m in mods_indices:
            mod = engine.analyze(relations, m, context + [index])
            if type(mod) is str:
                mods.append(mod)
            elif type(mod) is list:
                mods += mod

        return mods

    def extract(self, relations, index, context, engine, info={}):
        # Determiners
        det_index = Relation.get_children_with_dep('det', relations, index)
        if det_index == []:
            det = None
        else:
            det = engine.analyze(relations, det_index[0], context + [index])

        # Possessives
        poss_index = Relation.get_children_with_dep('poss', relations, index)
        if poss_index == []:
            poss = None
        else:
            poss = engine.analyze(relations, poss_index[0], context + [index])

        # Noun modifiers
        nn_indices = Relation.get_children_with_dep('nn', relations, index)
        nns = [engine.analyze(relations, i, context + [index])
               for i in nn_indices]

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

        # ADJP modifiers
        mods = NounPhraseRuleset.process_modifiers(relations, index, context,
                                                   engine, info)

        # VP modifiers
        prep_index = Relation.get_children_with_dep('prep', relations, index)
        if prep_index != []:
            engine.analyze(relations, prep_index[0], context + [index])

        # Emit propositions for modifiers

        # TODO: properly handle distribution of possessives.
        return_list = []
        ids_for_preconj = [] # Ids of propositions for reference by eventual
                             #  preconj propositions.
        for conj in conjs:
            if nns != []:
                if type(nns[0]) is str:
                    # Multiple nn modifying the same noun. Join to conj.
                    return_value = [word for word in [det, poss] +  nns + [conj]
                                    if word is not None]
                    return_list.append(' '.join(return_value))
                elif type(nns[0]) is list:
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

        for amod in mods:
            for noun in return_list:
                engine.emit((noun, amod))

        preconj_indices = Relation.get_children_with_dep('preconj', relations,
                                                         index)
        if preconj_indices != []:
            preconj = engine.analyze(relations, preconj_indices[0],
                                     context + [index])
        else:
            preconj = None

        return {'return_list': return_list,
                'preconj': preconj,
                'ids_for_preconj': ids_for_preconj}


class AdjectivalPhraseRuleset(Ruleset):
    """A base class for AdjP-like dependency substructures."""

    def extract(self, relations, index, context, engine, info={}):
        # TODO: complete. Add cc/conj handling.
        return [relations[index].word]


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


class AdvmodRuleset(AtomicEmittingRuleset):
    """A ruleset that processes the 'advmod' relation."""

    rel = 'advmod'


class NegRuleset(AtomicEmittingRuleset):
    """A ruleset that processes the 'neg' relation."""

    rel = 'neg'


# Noun-Phrase rulesets.


class NsubjRuleset(NounPhraseRuleset):
    """A ruleset that processes the 'nsubj' relation."""

    rel = 'nsubj'

    def extract(self, relations, index, context, engine, info={}):
        d = NounPhraseRuleset.extract(self, relations, index, context, engine,
                                      info)
        if d['ids_for_preconj'] == []:
            return d['return_list']


class NsubjpassRuleset(NounPhraseRuleset):
    """A ruleset that processes the 'nsubjpass' relation."""

    rel = 'nsubjpass'

    def extract(self, relations, index, context, engine, info={}):
        d = NounPhraseRuleset.extract(self, relations, index, context, engine,
                                      info)
        if d['ids_for_preconj'] == []:
            return d['return_list']


class DobjRuleset(NounPhraseRuleset):
    """A ruleset that processes the 'dobj' relation."""

    rel = 'dobj'

    def extract(self, relations, index, context, engine, info={}):
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
        d = NounPhraseRuleset.extract(self, relations, index, context,
                                      engine)
        if d['ids_for_preconj'] == []:
            for value in d['return_list']:
                engine.emit(('(to) ' + value,))


class ConjRuleset(NounPhraseRuleset):
    """A ruleset that processes the 'conj' relation."""

    rel = 'conj'

    def extract(self, relations, index, context, engine, info={}):
        d = NounPhraseRuleset.extract(self, relations, index, context,
                                      engine)
        if d['ids_for_preconj'] == []:
            return d['return_list']


class PossRuleset(NounPhraseRuleset):
    """A ruleset that processes the 'poss' relation."""

    rel = 'poss'

    def extract(self, relations, index, context, engine, info={}):
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


# Adjectival-Phrase rulesets


class AcompRuleset(AdjectivalPhraseRuleset):
    """A ruleset that processes the 'acomp' relation."""

    rel = 'acomp'


class AmodRuleset(AdjectivalPhraseRuleset):
    """A ruleset that processes the 'amod' relation."""

    rel = 'amod'


# Uncategorized rulesets.


class NnRuleset(Ruleset):
    """A ruleset that processes the 'nn' relation."""

    rel = 'nn'

    def extract(self, relations, index, context, engine, info={}):
        cc_indices = Relation.get_children_with_dep('cc', relations, index)

        if cc_indices != []:
            engine.analyze(relations, cc_indices[0], context + [index])
            conj_indices = Relation.get_children_with_dep('conj', relations,
                                                          index)
            conjs = [engine.analyze(relations, i, context + [index])
                     for i in conj_indices]
            conjs = [c[0] for c in conjs]
            # conjs = [c[0] for c in conjs]  # TODO: check if this makes sense.

            return [relations[index].word] + conjs
        else:
            return relations[index].word


class DetRuleset(Ruleset):
    """A ruleset that processes the 'det' relation."""

    rel = 'det'

    def extract(self, relations, index, context, engine, info={}):
        # TODO: check for cases like 'some', 'any', 'all', etc.
        if relations[index].word.lower() in ('the', 'a', 'an'):
            return relations[index].word.lower()
        else:
            # TODO: maybe get the subject from info.
            engine.emit((relations[context[-1]].word, relations[index].word))
            return None


class PrepRuleset(Ruleset):
    """A ruleset that processes the 'prep' relation."""

    rel = 'prep'

    def extract(self, relations, index, context, engine, info={}):
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
        number_indices = Relation.get_children_with_dep('possessive',
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

            if type(word) is str:
                words.append(word)
            elif type(word) is list:
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
        engine.emit((info['num'], relations[index].word))


all_rulesets = [TopRuleset(),
                # Verb-Phrase rulesets.
                RootRuleset(),
                XcompRuleset(),
                CcompRuleset(),
                PcompRuleset(),
                CsubjRuleset(),
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
                AdvmodRuleset(),
                NegRuleset(),
                # Noun-Phrase rulesets.
                NsubjRuleset(),
                NsubjpassRuleset(),
                DobjRuleset(),
                PobjRuleset(),
                IobjRuleset(),
                ConjRuleset(),
                PossRuleset(),
                # Adjectival-Phrase rulesets
                AcompRuleset(),
                AmodRuleset(),
                # Uncategorized rulesets.
                NnRuleset(),
                DetRuleset(),
                PrepRuleset(),
                QuantmodRuleset(),
                NumRuleset()]
