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
from idd3 import Ruleset
import logging


logger = logging.getLogger(__name__)


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

    def extract(self, relations, index, context, engine, info={}):
        logger.warning('The "complm" relation is not present in the Universal'
                       ' Dependencies, and is thus deprecated. It was replaced'
                       ' by "mark".')
        return super(ComplmRuleset, self).extract(relations, index, context,
                                                  engine, info)


class AdpRuleset(AtomicRuleset):

    """A ruleset that processes the 'adp' relation."""

    rel = 'adp'


class NumberRuleset(AtomicRuleset):

    """A ruleset that processes the 'number' relation."""

    rel = 'number'

    def extract(self, relations, index, context, engine, info={}):
        logger.warning('The "number" relation is not present in the Universal'
                       ' Dependencies, and is thus deprecated. It was replaced'
                       ' by "num".')
        return super(NumberRuleset, self).extract(relations, index, context,
                                                  engine, info)


class PreconjRuleset(AtomicRuleset):
    # TODO: Became 'cc'.

    """A ruleset that processes the 'preconj' relation."""

    rel = 'preconj'


class MarkRuleset(AtomicRuleset):

    """A ruleset that processes the 'mark' relation."""

    rel = 'mark'


class PredetRuleset(AtomicRuleset):
    # TODO: Became 'det'.

    """A ruleset that processes the 'predet' relation."""

    rel = 'predet'
