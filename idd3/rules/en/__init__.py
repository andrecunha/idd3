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

from idd3.base import Config
from idd3.rules.en import transform

# Atomic rulesets.
from idd3.rules.universal.atomic_rulesets import *

# Atomic emitting rulesets.
from idd3.rules.universal.atomic_emitting_rulesets import *

# Noun-Phrase rulesets.
from idd3.rules.universal.np_rulesets import *
from idd3.rules.en.np_rulesets import *

# Verb-Phrase rulesets.
from idd3.rules.universal.vp_rulesets import *

# Adjectival-Phrase rulesets
from idd3.rules.universal.adjp_rulesets import *

# Adverbial-Phrase rulesets
from idd3.rules.universal.advp_rulesets import *

# Uncategorized rulesets.
from idd3.rules.universal.misc_rulesets import *

all_rulesets = [TopRuleset(),
                # Atomic rulesets.
                PrtRuleset(),
                AuxRuleset(),
                AuxpassRuleset(),
                CcRuleset(),
                CopRuleset(),
                ComplmRuleset(),
                AdpRuleset(),
                NumberRuleset(),
                PreconjRuleset(),
                MarkRuleset(),
                PredetRuleset(),
                # Atomic emitting rulesets.
                NegRuleset(),
                DiscourseRuleset(),
                # Noun-Phrase rulesets.
                NsubjRuleset(),
                NsubjpassRuleset(),
                DobjRuleset(),
                AdpobjRuleset(),
                IobjRuleset(),
                PossRuleset(),
                NmodRuleset(),
                TmodRuleset(),
                ApposRuleset(),
                AttrRuleset(),
                # Verb-Phrase rulesets.
                RootRuleset(),
                XcompRuleset(),
                CcompRuleset(),
                AdpcompRuleset(),
                CsubjRuleset(),
                VmodRuleset(),
                AdvclRuleset(),
                RcmodRuleset(),
                ParataxisRuleset(),
                # Adjectival-Phrase rulesets
                AcompRuleset(),
                AmodRuleset(),
                # Adverbial-Phrase rulesets
                AdvmodRuleset(),
                # Uncategorized rulesets.
                ConjRuleset(),
                CompmodJoinRuleset(),
                DetRuleset(),
                AdpmodRuleset(),
                NumRuleset(),
                WhatRuleset(),
                CompmodRuleset()]

config = Config()

NON_EMITTED_DETS = ('the', 'a', 'an', 'this', 'these', 'that', 'those')
RELATIVE_PRONOUNS = ('that', 'which', 'who')
GERUND_TAGS = ('VBG')

config.from_object(__name__)

all_transformations = transform.all_transformations
