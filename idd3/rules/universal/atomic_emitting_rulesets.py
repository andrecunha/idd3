# -*- coding: utf-8 -*-
# IDD3 - Propositional Idea Density from Dependency Trees
# Copyright (C) 2014-2015  Andre Luiz Verucci da Cunha
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


class AtomicEmittingRuleset(Ruleset):

    """A base ruleset for atomic relations that just emits the associated word
    as a proposition."""

    def extract(self, relations, index, context, engine, info={}):
        engine.emit((relations[index].word,))


class NegRuleset(AtomicEmittingRuleset):

    """A ruleset that processes the 'neg' relation."""

    rel = 'neg'

    def extract(self, relations, index, context, engine, info={}):
        engine.emit((relations[index].word,), 'M')


class DiscourseRuleset(AtomicEmittingRuleset):

    """A ruleset that processes the 'discourse' relation."""

    rel = 'discourse'

    def extract(self, relations, index, context, engine, info={}):
        engine.emit((relations[index].word,), 'M')


