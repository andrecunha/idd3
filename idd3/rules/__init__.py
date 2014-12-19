# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division

# Atomic rulesets.
from idd3.rules.atomic_rulesets import *

# Atomic emitting rulesets.
from idd3.rules.atomic_emitting_rulesets import *

# Noun-Phrase rulesets.
from idd3.rules.np_rulesets import *

# Verb-Phrase rulesets.
from idd3.rules.vp_rulesets import *

# Adjectival-Phrase rulesets
from idd3.rules.adjp_rulesets import *

# Adverbial-Phrase rulesets
from idd3.rules.advp_rulesets import *

# Uncategorized rulesets.
from idd3.rules.misc_rulesets import *

all_rulesets = [TopRuleset(),
                # Atomic rulesets.
                PrtRuleset(),
                AuxRuleset(),
                AuxpassRuleset(),
                CcRuleset(),
                CopRuleset(),
                ComplmRuleset(),
                PossessiveRuleset(),
                NumberRuleset(),
                PreconjRuleset(),
                MarkRuleset(),
                # Atomic emitting rulesets.
                NegRuleset(),
                DiscourseRuleset(),
                # Noun-Phrase rulesets.
                NsubjRuleset(),
                NsubjpassRuleset(),
                DobjRuleset(),
                PobjRuleset(),
                IobjRuleset(),
                PossRuleset(),
                NpadvmodRuleset(),
                TmodRuleset(),
                ApposRuleset(),
                # Verb-Phrase rulesets.
                RootRuleset(),
                XcompRuleset(),
                CcompRuleset(),
                PcompRuleset(),
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
                NnRuleset(),
                DetRuleset(),
                PrepRuleset(),
                QuantmodRuleset(),
                NumRuleset()]
