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


class RemoveParataxisFillers(Transformation):
    """Removes lexical fillers like 'I mean'."""

    def transform(self, relations):
        for i, relation in enumerate(relations):
            if relation.rel == 'parataxis':
                if relation.word == 'mean' \
                        and len(relation.deps) == 1\
                        and relations[relation.deps[0]].word == "I":
                    delete_indices(relations, [i, relation.deps[0]])


class RemoveUtteranceInitialConjunction(Transformation):
    """Removes commonly used utterance-initial conjuntions (and, then)."""

    def transform(self, relations):
        if relations[1].word.lower() in ('and', 'then'):
            delete_indices(relations, [1])


class JoinNoLonger(Transformation):

    """Joins 'no longer' as a multiword expression."""

    def transform(self, relations):
        for i in range(len(relations)):
            if relations[i].word == 'no' and relations[i + 1].word == 'longer':
                relations[i].rel = 'mwe'
                relations[i + 1].rel = 'neg'


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


class JoinDoublePrepositions(Transformation):

    """Handles double prepositions, as in 'As of 2014'."""

    def transform(self, relations):
        indices_to_delete = []

        for i in range(len(relations)):
            if relations[i].tag == "IN":
                if i + 1 < len(relations) and relations[i + 1].tag == "IN":
                    relations[i].word += ' ' + relations[i + 1].word

                    for j in range(i + 1, len(relations)):
                        if relations[j].head == i + 1:
                            relations[j].head = i
                            relations[i].deps.append(j)

                    relations[i].deps.sort()
                    indices_to_delete.append(i + 1)

        delete_indices(relations, indices_to_delete)


class JoinExpletives(Transformation):

    """Handles expletives, as in 'there is', or 'there are'."""

    def transform(self, relations):
        indices_to_delete = []

        for i in range(len(relations)):
            if relations[i].tag == "EX":
                relations[i + 1].word = relations[i].word +\
                    ' ' + relations[i + 1].word
                indices_to_delete.append(i)

        delete_indices(relations, indices_to_delete)


class FixAdjectiveRepetition(Transformation):

    """Handles adjective repetition as intensifier (e.g., she was gone a long
        long time.). In this case, the first adjective is turned into an
        adverb and connected to the second adjective."""

    def transform(self, relations):
        for i in range(len(relations)):
            if relations[i].tag == 'JJ':
                if i + 1 < len(relations)\
                        and relations[i + 1].tag == 'JJ'\
                        and relations[i + 1].word == relations[i].word\
                        and relations[i + 1].head == relations[i].head\
                        and relations[i + 1].rel == relations[i].rel:
                    relations[i].tag = 'RB'
                    relations[i].head = i + 1
                    relations[i].rel = 'advmod'
                    relations[i + 1].deps.append(i)


class FixAdverbRepetition(Transformation):

    """Handles adverb repetition as intensifier (e.g., he is very very sick).
        In this case, we make sure the first adverb is connected to the second,
        not to the following word (usually an adjective)."""

    def transform(self, relations):
        for i in range(len(relations)):
            if relations[i].tag == 'RB':
                if i + 1 < len(relations)\
                        and relations[i + 1].tag == 'RB'\
                        and relations[i + 1].word == relations[i].word\
                        and relations[i + 1].rel == relations[i].rel\
                        and relations[i].head != i + 1:
                    relations[i].head = i + 1
                    relations[i + 1].deps.append(i)
                    relations[i + 1].deps.sort()


class FixReflexivePronouns(Transformation):

    """Handles reflexive pronouns following nouns. Here, we connect the
        pronoun to the previous noun as an adjectival modifier."""

    reflexive_pronouns = ['myself', 'yourself', 'himself', 'herself', 'itself',
                          'ourselves', 'yourselves', 'themselves']

    def transform(self, relations):
        for i in range(len(relations)):
            if relations[i].tag == 'PRP'\
                    and relations[i].word in self.reflexive_pronouns\
                    and relations[i - 1].tag in ('NN', 'NNS', 'NNP', 'NNPS'):
                relations[relations[i].head].deps.remove(i)
                relations[i].head = i - 1
                relations[i].rel = 'amod'
                relations[i - 1].deps.append(i)
                relations[i - 1].deps.sort()


all_transformations = [RemovePunctuation(),
                       RemoveParataxisFillers(),
                       RemoveUtteranceInitialConjunction(),
                       JoinNoLonger(),
                       JoinMultiWordExpressions(),
                       JoinPhrasalModifiers(),
                       JoinDoublePrepositions(),
                       JoinExpletives(),
                       FixAdjectiveRepetition(),
                       FixAdverbRepetition(),
                       FixReflexivePronouns()]
