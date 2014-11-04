# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Ruleset


# Base classes.


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


class VerbPhraseRuleset(Ruleset):
    """A base class for VP-like dependency substructures."""

    @staticmethod
    def process_subject(relations, index, context, engine, info):
        """TODO: Docstring for process_subject.

        :relations: TODO
        :index: TODO
        :context: TODO
        :engine: TODO
        :info: TODO
        :returns: TODO

        """
        # TODO: handle clausal subjects.
        subj_index = Relation.get_children_with_dep('nsubj', relations, index)
        if subj_index == []:
            if relations[index].rel == 'xcomp':
                subj = ['(%s)' % info['subj']]
            else:
                subj = ['NO_NSUBJ']
        else:
            subj = engine.analyze(relations, subj_index[0], context + [index])

        return subj

    @staticmethod
    def process_auxiliaries(relations, index, context, engine, info):
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
        if aux_index == []:
            aux = None
        else:
            aux = engine.analyze(relations, aux_index[0], context + [index])

        return aux

    @staticmethod
    def process_particles(relations, index, context, engine, info):
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
    def process_dobj(relations, index, context, engine, info):
        """todo: docstring for process_subject.

        :relations: todo
        :index: todo
        :context: todo
        :engine: todo
        :info: todo
        :returns: todo

        """
        dobj_index = Relation.get_children_with_dep('dobj', relations, index)
        if dobj_index == []:
            dobj = []
        else:
            dobj = engine.analyze(relations, dobj_index[0], context + [index])

        return dobj

    @staticmethod
    def process_xcomp(relations, index, context, engine, info):
        """todo: docstring for process_subject.

        :relations: todo
        :index: todo
        :context: todo
        :engine: todo
        :info: todo
        :returns: todo

        """
        xcomp_index = Relation.get_children_with_dep('xcomp', relations, index)
        if xcomp_index != []:
            engine.analyze(relations, xcomp_index[0], context + [index], info)

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
    def process_advmods(relations, index, context, engine, info):
        """todo: docstring for process_advmods.

        :relations: todo
        :index: todo
        :context: todo
        :engine: todo
        :info: todo
        :returns: todo

        """
        advmod_indices = Relation.get_children_with_dep('advmod', relations,
                                                        index)
        for i in advmod_indices:
            engine.analyze(relations, i, context + [index])

    def extract(self, relations, index, context, engine, info={}):
        # TODO: handle other VB tags.
        if relations[index].tag in ('VBZ', 'VBD', 'VBN', 'VB', 'VBG'):
            subjs = self.process_subject(relations, index, context, engine,
                                         info)

            aux = self.process_auxiliaries(relations, index, context, engine,
                                           info)

            prt = self.process_particles(relations, index, context, engine,
                                         info)
            verb = ' '.join([word for word in [aux, relations[index].word, prt]
                             if word is not None])

            dobjs = self.process_dobj(relations, index, context, engine, info)

            self.process_xcomp(relations, index, context, engine,
                               {'subj': subjs[0]})  # TODO: change this.

            self.process_ccomp(relations, index, context, engine,
                               {'subj': subjs[0]})  # TODO: change this.

            self.process_iobj(relations, index, context, engine, info)

            self.process_advmods(relations, index, context, engine, info)

            # Emit propositions.
            for subj in subjs:
                if len(dobjs) > 0:
                    for dobj in dobjs:
                        proposition = tuple([w for w in [verb, subj, dobj]])
                        engine.emit(proposition)
                else:
                    engine.emit((verb, subj))

            return relations[index].word
        elif relations[index].tag in ('NN'):
            print('### JUST TEST !!! ###')
            engine.emit((relations[index].word,))
        else:
            print('VP: cannot handle', relations[index].tag, 'yet.')


class AtomicRuleset(Ruleset):
    """A base ruleset for atomic relations, that just return the associated
    word."""

    def extract(self, relations, index, context, engine, info={}):
        return relations[index].word


# Derived classes.


class TopRuleset(Ruleset):
    """A dummy ruleset that starts the analysis process."""

    rel = 'TOP'

    def extract(self, relations, index, context, engine, info={}):
        return engine.analyze(relations, relations[index].deps[0])


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


class PossRuleset(AtomicRuleset):
    """A ruleset that processes the 'poss' relation."""

    rel = 'poss'


class CcRuleset(AtomicRuleset):
    """A ruleset that processes the 'cc' relation."""

    rel = 'cc'


class AdvmodRuleset(AtomicRuleset):
    """A ruleset that processes the 'advmod' relation."""

    rel = 'advmod'

    def extract(self, relations, index, context, engine, info={}):
        value = AtomicRuleset.extract(self, relations, index, context, engine)
        engine.emit((value, ))


# Noun-Phrase rulesets.


class NsubjRuleset(NounPhraseRuleset):
    """A ruleset that processes the 'nsubj' relation."""

    rel = 'nsubj'


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
        if pobj_index == []:
            print('PREP: prep without pobj!')
        else:
            pobjs = engine.analyze(relations, pobj_index[0], context + [index])
            for pobj in pobjs:
                engine.emit((relations[index].word + ' ' + pobj,))


all_rulesets = [TopRuleset(),
                RootRuleset(),
                XcompRuleset(),
                CcompRuleset(),
                PrtRuleset(),
                NnRuleset(),
                AuxRuleset(),
                PossRuleset(),
                CcRuleset(),
                AdvmodRuleset(),
                NsubjRuleset(),
                DobjRuleset(),
                PobjRuleset(),
                IobjRuleset(),
                ConjRuleset(),
                DetRuleset(),
                PrepRuleset()]
