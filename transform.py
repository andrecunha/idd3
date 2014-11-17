# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Transformation


class JoinPhrasalModifiers(Transformation):
    """Joins phrasal modal and aspectual markers (e.g., "have to", "ought to",
        "used to", etc) to the main verb of a sentence. """

    verb_forms = ['have', 'has', 'had', 'ought', 'use', 'uses', 'used']

    def transform(self, relations):
        for index, relation in enumerate(relations):
            if relation.rel in ('null', 'xcomp')\
                    and relation.tag in ('VBZ', 'VBD', 'VBP')\
                    and relation.word in self.verb_forms:
                xcomp_index = Relation.get_children_with_dep('xcomp',
                                                             relations,
                                                             index)[0]
                if relations[xcomp_index].tag == 'VB':
                    aux_indices = Relation.get_children_with_dep('aux',
                                                                 relations,
                                                                 xcomp_index)
                    to_index = [index for index in aux_indices
                                if relations[index].tag == 'TO'][0]

                    # Append 'to' and the xcomp head to main verb.
                    relations[index].word += ' to ' + \
                        relations[xcomp_index].word

                    # Remove 'to' and xcomp head.
                    indices_to_remove = sorted([to_index, xcomp_index],
                                               reverse=True)
                    for i in indices_to_remove:
                        del relations[i]

                    for i, rel in enumerate(relations):
                        rel.address = i

                    # Change head of relations pointing to xcomp to point to
                    #   the main verb. Remove xcomp head from main verb's deps.
                    for i, rel in enumerate(relations):
                        if rel.head == xcomp_index:
                            rel.head = index
                            relations[index].deps.append(i)

                    relations[index].deps.remove(xcomp_index)

                    relations[index].deps = sorted(relations[index].deps)

                    # Update indices in deps.
                    for rel in relations:
                        for i, dep in enumerate(rel.deps):
                            if dep > xcomp_index:
                                rel.deps[i] -= 2


all_transformations = [JoinPhrasalModifiers(),]
