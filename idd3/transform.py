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
from idd3.base import Transformation


def delete_indices(relations, indices):
    """Removes relations in place. This function does NOT change the head of
        eventual relations that point to a removed relation; these head updates
        have to be done elsewhere.

    :relations: the list of relations in a utterance.
    :indices: the indices of the relations to remove.

    """
    indices = sorted(indices, reverse=True)

    for index in indices:
        del relations[index]

        for rel in relations:
            if rel.head is not None:
                if rel.head >= index:
                    rel.head -= 1

    for i, rel in enumerate(relations):
        rel.address = i
        rel.deps = []

    for i, rel in enumerate(relations):
        if rel.head is not None:
            relations[rel.head].deps.append(i)

    for rel in relations:
        rel.deps.sort()


class RemovePunctuation(Transformation):
    """Removes punct relations."""

    def transform(self, relations):
        indices_to_remove = []
        for i, relation in enumerate(relations):
            if relation.rel == 'p':
                indices_to_remove.append(i)
        delete_indices(relations, indices_to_remove)
