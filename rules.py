# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Ruleset


class TopRuleset(Ruleset):
    """A dummy ruleset that starts the analysis process."""

    def __init__(self):
        Ruleset.__init__(self, 'TOP')

    def extract(self, relations, index, context, engine):
        return engine.analyze(relations, relations[index].deps[0])


class RootRuleset(Ruleset):
    """A ruleset that processes the 'ROOT' relation."""

    def __init__(self):
        Ruleset.__init__(self, 'null')

    def extract(self, relations, index, context, engine):
        pass


class NsubjRuleset(Ruleset):
    """A ruleset that processes the 'nsubj' relation."""

    def __init__(self):
        Ruleset.__init__(self, 'nsubj')

    def extract(self, relations, index, context, engine):
        pass


class DetRuleset(Ruleset):
    """A ruleset that processes the 'det' relation."""

    def __init__(self):
        Ruleset.__init__(self, 'det')

    def extract(self, relations, index, context, engine):
        pass

all_rulesets = [TopRuleset(),
                RootRuleset(),
                NsubjRuleset(),
                DetRuleset()]
