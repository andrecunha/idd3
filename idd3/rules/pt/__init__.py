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

from idd3.base import Config
from idd3.rules.pt import transform
from idd3.rules import universal

config = Config()

NON_EMITTED_DETS = ('the', 'a', 'an', 'this', 'these', 'that', 'those')
NON_EMITTED_DETS = ('o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
                    'este', 'esta', 'estes', 'estas',
                    'esse', 'essa', 'esses', 'essas',
                    'aquele', 'aquela', 'aqueles', 'aquelas')
RELATIVE_PRONOUNS = ('que', 'onde', 'cujo', 'cuja', 'cujos', 'cujas')
GERUND_TAGS = ()

config.from_object(__name__)

all_transformations = transform.all_transformations
all_rulesets = universal.all_rulesets
