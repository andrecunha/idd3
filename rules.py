# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Ruleset


class TopRuleset(Ruleset):
    """A dummy ruleset that starts the analysis process."""

    rel = 'TOP'

    def extract(self, relations, index, context, engine):
        return engine.analyze(relations, relations[index].deps[0])


class RootRuleset(Ruleset):
    """A ruleset that processes the 'ROOT' relation."""

    rel = 'null'

    def extract(self, relations, index, context, engine):
        # TODO: handle other VB tags.
        if relations[index].tag in ('VBZ', 'VBD'):
            # TODO: handle clausal subjects.
            subj_index = Relation.get_child_with_dep('nsubj', relations, index)

            if subj_index is None:
                subj = 'NO_NSUBJ'
            else:
                subj = engine.analyze(relations, subj_index, context + [index])

            engine.emit((relations[index].word, subj))

            return relations[index].word
        else:
            print('ROOT: cannot handle', relations[index].tag, 'yet.')


class NsubjRuleset(Ruleset):
    """A ruleset that processes the 'nsubj' relation."""

    rel = 'nsubj'

    def extract(self, relations, index, context, engine):
        det_index = Relation.get_child_with_dep('det', relations, index)

        if det_index is None:
            return relations[index].word
        else:
            det = engine.analyze(relations, det_index, context + [index])
            return (det + ' ' if det != '' else '') + relations[index].word


class DetRuleset(Ruleset):
    """A ruleset that processes the 'det' relation."""

    rel = 'det'

    def extract(self, relations, index, context, engine):
        # TODO: check for cases like 'some', 'any', 'all', etc.
        if relations[index].word in ('the', 'a', 'an'):
            return relations[index].word
        else:
            print('DET: complete DT rules!')
            return ''


all_rulesets = [TopRuleset(),
                RootRuleset(),
                NsubjRuleset(),
                DetRuleset()]
