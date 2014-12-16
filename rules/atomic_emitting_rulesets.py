# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Ruleset


class AtomicEmittingRuleset(Ruleset):

    """A base ruleset for atomic relations that just emits the associated word
    as a proposition."""

    def extract(self, relations, index, context, engine, info={}):
        engine.emit((relations[index].word,))


class NegRuleset(AtomicEmittingRuleset):

    """A ruleset that processes the 'neg' relation."""

    rel = 'neg'


class DiscourseRuleset(AtomicEmittingRuleset):

    """A ruleset that processes the 'discourse' relation."""

    rel = 'discourse'