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
        prep_index = Relation.get_children_with_dep('prep', relations, index)
        if prep_index != []:
            engine.analyze(relations, prep_index[0], context + [index])

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

    def extract(self, relations, index, context, engine, info={}):
        det_index = Relation.get_children_with_dep('det', relations, index)
        if det_index == []:
            det = None
        else:
            det = engine.analyze(relations, det_index[0], context + [index])

        poss_index = Relation.get_children_with_dep('poss', relations, index)
        if poss_index == []:
            poss = None
        else:
            poss = engine.analyze(relations, poss_index[0], context + [index])

        # TODO: multiple nn.
        nn_index = Relation.get_children_with_dep('nn', relations, index)
        if nn_index == []:
            nn = None
        else:
            nn = engine.analyze(relations, nn_index[0], context + [index])

        cc_index = Relation.get_children_with_dep('cc', relations, index)
        if cc_index != []:
            engine.analyze(relations, cc_index[0], context + [index])
            conj_index = Relation.get_children_with_dep('conj', relations,
                                                        index)
            conjs = [engine.analyze(relations, i, context + [index])
                     for i in conj_index]
            conjs = [c[0] for c in conjs]  # TODO: check if this makes sense.

        else:
            conjs = []
        conjs = [relations[index].word] + conjs

        return_list = []
        for conj in conjs:
            return_value = [word for word in [det, poss, nn, conj]
                            if word is not None]
            return_list.append(' '.join(return_value))

        return return_list


class AdjectivalPhraseRuleset(Ruleset):
    """A base class for AdjP-like dependency substructures."""

    def extract(self, relations, index, context, engine, info={}):
        # TODO: complete.
        return relations[index].word


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


class NnRuleset(AtomicRuleset):
    """A ruleset that processes the 'nn' relation."""

    rel = 'nn'


class AuxRuleset(AtomicRuleset):
    """A ruleset that processes the 'aux' relation."""

    rel = 'aux'


class AuxpassRuleset(AtomicRuleset):
    """A ruleset that processes the 'auxpass' relation."""

    rel = 'auxpass'


class PossRuleset(AtomicRuleset):
    """A ruleset that processes the 'poss' relation."""

    rel = 'poss'


class CcRuleset(AtomicRuleset):
    """A ruleset that processes the 'cc' relation."""

    rel = 'cc'


class CopRuleset(AtomicRuleset):
    """A ruleset that processes the 'cop' relation."""

    rel = 'cop'


class ComplmRuleset(AtomicRuleset):
    """A ruleset that processes the 'complm' relation."""

    rel = 'complm'


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


class NsubjpassRuleset(NounPhraseRuleset):
    """A ruleset that processes the 'nsubjpass' relation."""

    rel = 'nsubjpass'


class DobjRuleset(NounPhraseRuleset):
    """A ruleset that processes the 'dobj' relation."""

    rel = 'dobj'


class PobjRuleset(NounPhraseRuleset):
    """A ruleset that processes the 'pobj' relation."""

    rel = 'pobj'


class IobjRuleset(NounPhraseRuleset):
    """A ruleset that processes the 'iobj' relation."""

    rel = 'iobj'

    def extract(self, relations, index, context, engine, info={}):
        values = NounPhraseRuleset.extract(self, relations, index, context,
                                           engine)
        for value in values:
            engine.emit(('(to) ' + value,))


class ConjRuleset(NounPhraseRuleset):
    """A ruleset that processes the 'conj' relation."""

    rel = 'conj'


# Adjectival-Phrase rulesets


class AcompRuleset(AdjectivalPhraseRuleset):
    """A ruleset that processes the 'acomp' relation."""

    rel = 'acomp'


# Uncategorized rulesets.


class DetRuleset(Ruleset):
    """A ruleset that processes the 'det' relation."""

    rel = 'det'

    def extract(self, relations, index, context, engine, info={}):
        # TODO: check for cases like 'some', 'any', 'all', etc.
        if relations[index].word.lower() in ('the', 'a', 'an'):
            return relations[index].word.lower()
        else:
            print('DET: complete DT rules!')
            return ''


class PrepRuleset(Ruleset):
    """A ruleset that processes the 'prep' relation."""

    rel = 'prep'

    def extract(self, relations, index, context, engine, info={}):
        pobj_index = Relation.get_children_with_dep('pobj', relations, index)
        if pobj_index != []:
            pobjs = engine.analyze(relations, pobj_index[0], context + [index])
            for pobj in pobjs:
                engine.emit((relations[index].word + ' ' + pobj,))

        pcomp_index = Relation.get_children_with_dep('pcomp', relations, index)
        if pcomp_index != []:
            pcomp = engine.analyze(relations, pcomp_index[0],
                                   context + [index])
            if pcomp is not None:
                engine.emit((relations[index].word + ' ' + pcomp,))
            # TODO: check the 'else' condition.


all_rulesets = [TopRuleset(),
                # Verb-Phrase rulesets.
                RootRuleset(),
                XcompRuleset(),
                CcompRuleset(),
                PcompRuleset(),
                CsubjRuleset(),
                # Atomic rulesets.
                PrtRuleset(),
                NnRuleset(),
                AuxRuleset(),
                AuxpassRuleset(),
                PossRuleset(),
                CcRuleset(),
                CopRuleset(),
                ComplmRuleset(),
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
                # Adjectival-Phrase rulesets
                AcompRuleset(),
                # Uncategorized rulesets.
                DetRuleset(),
                PrepRuleset()]
