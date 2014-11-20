# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Transformation


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
            rel.deps = [dep for dep in rel.deps if dep != index]

            for i, dep in enumerate(rel.deps):
                if dep > index:
                    rel.deps[i] -= 1

            if rel.head is not None:
                if rel.head > index:
                    rel.head -= 1

    for i, rel in enumerate(relations):
        rel.address = i


class RemovePunctuation(Transformation):
    """Removes punct relations."""

    def transform(self, relations):
        indices_to_remove = []
        for i, relation in enumerate(relations):
            if relation.rel == 'punct':
                indices_to_remove.append(i)
        delete_indices(relations, indices_to_remove)


class JoinMultiWordExpressions(Transformation):
    """Joins multi-word expressions in a single node. """

    def transform(self, relations):
        mwes = {}

        for relation in relations:
            if relation.rel == 'mwe':
                if relation.head not in mwes:
                    mwes[relation.head] = [relation.address]
                else:
                    mwes[relation.head].append(relation.address)

        for head, deps in mwes.items():
            new_word = ' '.join([relations[i].word
                                 for i in sorted(deps + [head])])
            relations[head].word = new_word

            delete_indices(relations, deps)


class JoinPhrasalModifiers(Transformation):
    """Joins phrasal modal and aspectual markers (e.g., "have to", "ought to",
        "used to", etc) to the main verb of a sentence. """

    verb_forms = ['have', 'has', 'had', 'ought', 'use', 'uses', 'used']

    def transform(self, relations):
        for index, relation in enumerate(relations):
            if relation.rel in ('null', 'xcomp')\
                    and relation.tag in ('VBZ', 'VBD', 'VBP')\
                    and relation.word in self.verb_forms:
                xcomp_indices = Relation.get_children_with_dep('xcomp',
                                                               relations,
                                                               index)
                if xcomp_indices == []:
                    return
                else:
                    xcomp_index = xcomp_indices[0]

                if relations[xcomp_index].tag == 'VB':
                    aux_indices = Relation.get_children_with_dep('aux',
                                                                 relations,
                                                                 xcomp_index)
                    to_index = [index for index in aux_indices
                                if relations[index].tag == 'TO'][0]

                    # Append 'to' and the xcomp head to main verb.
                    relations[index].word += ' to ' + \
                        relations[xcomp_index].word

                    # Remove 'aux' and 'xcomp' relations.
                    delete_indices(relations, [to_index, xcomp_index])

                    # Change head of relations pointing to xcomp to point to
                    #   the main verb.
                    for i, rel in enumerate(relations):
                        if rel.head == xcomp_index:
                            rel.head = index
                            relations[index].deps.append(i)

                    relations[index].deps = sorted(relations[index].deps)


all_transformations = [RemovePunctuation(),
                       JoinPhrasalModifiers(),
                       JoinMultiWordExpressions()]
