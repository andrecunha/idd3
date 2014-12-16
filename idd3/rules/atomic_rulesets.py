# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Ruleset


class AtomicRuleset(Ruleset):

    """A base ruleset for atomic relations that just returns the associated
    word."""

    def extract(self, relations, index, context, engine, info={}):
        return relations[index].word


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