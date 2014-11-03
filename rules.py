# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Ruleset


# Base classes.


class NounPhraseRuleset(Ruleset):
    """A base class for NP-like dependency substructures."""

    def extract(self, relations, index, context, engine):
        det_index = Relation.get_child_with_dep('det', relations, index)
        if det_index is None:
            det = None
        else:
            det = engine.analyze(relations, det_index, context + [index])

        # TODO: multiple nn.
        nn_index = Relation.get_child_with_dep('nn', relations, index)
        if nn_index is None:
            nn = None
        else:
            nn = engine.analyze(relations, nn_index, context + [index])

        return_value = [word for word in [det, nn, relations[index].word]
                        if word is not None]
        return ' '.join(return_value)


class AtomicRuleset(Ruleset):
    """A base ruleset for atomic relations, that just return the associated
    word."""

    def extract(self, relations, index, context, engine):
        return relations[index].word


# Derived classes.


class TopRuleset(Ruleset):
    """A dummy ruleset that starts the analysis process."""

    rel = 'TOP'

    def extract(self, relations, index, context, engine):
        return engine.analyze(relations, relations[index].deps[0])


# Verb-Phrase rulesets.


class RootRuleset(Ruleset):
    """A ruleset that processes the 'ROOT' relation."""

    rel = 'null'

    def extract(self, relations, index, context, engine):
        # TODO: handle other VB tags.
        if relations[index].tag in ('VBZ', 'VBD', 'VBN'):
            # Process subject.

            # TODO: handle clausal subjects.
            subj_index = Relation.get_child_with_dep('nsubj', relations, index)
            if subj_index is None:
                subj = 'NO_NSUBJ'
            else:
                subj = engine.analyze(relations, subj_index, context + [index])

            # Process auxiliaries.
            aux_index = Relation.get_child_with_dep('aux', relations, index)
            if aux_index is None:
                aux = None
            else:
                aux = engine.analyze(relations, aux_index, context + [index])

            # Process phrasal verb particle.
            prt_index = Relation.get_child_with_dep('prt', relations, index)
            if prt_index is None:
                prt = None
            else:
                prt = engine.analyze(relations, prt_index, context + [index])
            verb = ' '.join([word for word in [aux, relations[index].word, prt]
                             if word is not None])

            # Process direct object.
            dobj_index = Relation.get_child_with_dep('dobj', relations, index)
            if dobj_index is None:
                dobj = None
            else:
                dobj = engine.analyze(relations, dobj_index, context + [index])

            # Process indirect object.

            # prep + pobj
            prep_index = Relation.get_child_with_dep('prep', relations, index)
            if prep_index is not None:
                engine.analyze(relations, prep_index, context + [index])

            # Emit proposition.
            if dobj is None:
                engine.emit((verb, subj))
            else:
                engine.emit((verb, subj, dobj))

            return relations[index].word
        else:
            print('ROOT: cannot handle', relations[index].tag, 'yet.')


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


# Uncategorized rulesets.


class DetRuleset(Ruleset):
    """A ruleset that processes the 'det' relation."""

    rel = 'det'

    def extract(self, relations, index, context, engine):
        # TODO: check for cases like 'some', 'any', 'all', etc.
        if relations[index].word.lower() in ('the', 'a', 'an'):
            return relations[index].word.lower()
        else:
            print('DET: complete DT rules!')
            return ''


class PrepRuleset(Ruleset):
    """A ruleset that processes the 'prep' relation."""

    rel = 'prep'

    def extract(self, relations, index, context, engine):
        pobj_index = Relation.get_child_with_dep('pobj', relations, index)
        if pobj_index is None:
            print('PREP: prep without pobj!')
        else:
            pobj = engine.analyze(relations, pobj_index, context + [index])
            engine.emit((relations[index].word + ' ' + pobj,))

all_rulesets = [TopRuleset(),
                RootRuleset(),
                PrtRuleset(),
                NnRuleset(),
                AuxRuleset(),
                NsubjRuleset(),
                DobjRuleset(),
                PobjRuleset(),
                DetRuleset(),
                PrepRuleset()]
