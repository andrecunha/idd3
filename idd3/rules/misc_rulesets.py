# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, division
from idd3 import Relation, Ruleset


class TopRuleset(Ruleset):

    """A dummy ruleset that starts the analysis process."""

    rel = 'TOP'

    def extract(self, relations, index, context, engine, info={}):
        return engine.analyze(relations, relations[index].deps[0], [index])
 

class NnRuleset(Ruleset):

    """A ruleset that processes the 'nn' relation."""

    rel = 'nn'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> str | list(str)

        An nn can be a single word or multiple words connected by cc/conj.

        Examples:

            * Oil prices
                nn(prices, Oil)
                -> return "Oil"
            * East and West Germany
                nn(Germany, East)
                cc(East, and)
                conj(East, West)
                -> return ["East", "West"]
        """
        cc_indices = Relation.get_children_with_dep('cc', relations, index)

        if cc_indices != []:
            engine.analyze(relations, cc_indices[0], context + [index])
            conj_indices = Relation.get_children_with_dep('conj', relations,
                                                          index)
            conjs = [engine.analyze(relations, i, context + [index])
                     for i in conj_indices]
            conjs = [c[0] for c in conjs]  # TODO: check if this makes sense.

            return [relations[index].word] + conjs
        else:
            return relations[index].word


class DetRuleset(Ruleset):

    """A ruleset that processes the 'det' relation."""

    rel = 'det'

    non_emitted_dets = ('the', 'a', 'an', 'this', 'these')

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> str | None

        A determiner may or may not emit a new proposition. Determiners like
            the, a, an, this, and these get joined to the noun they precede;
            others, like some and any, generate their own proposition.

        Examples:

            * The apple
                det(apple, The)
                -> return "The"

            * Some apples
                det(apple, some)
                -> emit((apple, some))
                -> return None
        """
        if relations[index].word.lower() in self.non_emitted_dets:
            return relations[index].word
        else:
            # TODO: maybe get the subject from info.
            engine.emit((relations[context[-1]].word, relations[index].word))
            return None


class PrepRuleset(Ruleset):

    """A ruleset that processes the 'prep' relation."""

    rel = 'prep'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> None

        Prepositional phrases always generate new propositions, according to
            Chand et al.'s manual.

        Examples:

            * to the city
                pobj(to, city)
                det(city, the)
                -> emit((to the city,))

            * to both East and West Germany
                pobj(to, Germany)
                preconj(Germany, both)
                nn(Germany, East)
                cc(East, and)
                conj(East, West)
                -> emit((to East Germany, )) # Proposition x
                -> emit((to West Germany, )) # Proposition y
                -> emit((both, x, y))

            * TODO: insert example with PCOMP.
        """
        # pobj
        pobj_index = Relation.get_children_with_dep('pobj', relations, index)
        if pobj_index != []:
            pobjs = engine.analyze(relations, pobj_index[0], context + [index])

            emitted_prop_ids = []
            for pobj in pobjs['return_list']:
                prop_id = engine.emit((relations[index].word + ' ' + pobj,))
                emitted_prop_ids.append(prop_id)

            if pobjs['ids_for_preconj'] != []:
                indices = [j for i, j in enumerate(emitted_prop_ids)
                           if i in pobjs['ids_for_preconj']]
                proposition = tuple([pobjs['preconj']] + indices)
                engine.emit(proposition)

        # pcomp
        pcomp_index = Relation.get_children_with_dep('pcomp', relations, index)
        if pcomp_index != []:
            pcomp = engine.analyze(relations, pcomp_index[0],
                                   context + [index])
            if pcomp is not None:
                engine.emit((relations[index].word + ' ' + pcomp,))
            # TODO: check the 'else' condition.


class NumRuleset(Ruleset):

    """A ruleset that processes the 'num' relation."""

    rel = 'num'

    def extract(self, relations, index, context, engine, info={}):
        """extract(relations, index, context, engine, info) -> str

        Nummerical modifiers are treated in the same way as adjectives.
            This ruleset assembles and returns the number, and it's up
            to the calling NounPhraseRuleset to emit the propositions.
            This ruleset also emits propositions for quantifier phrase
            modifiers.

        Examples:

            * About 200 people
                num(people, 200)
                quantmod(200, About)
                -> emit((200, about)) # by calling QuantmodRuleset
                -> return "200"
        """
        number_indices = Relation.get_children_with_dep('number',
                                                        relations, index)
        cc_indices = Relation.get_children_with_dep('cc',
                                                    relations, index)
        conj_indices = Relation.get_children_with_dep('conj',
                                                      relations, index)

        indices = sorted([index] + number_indices + cc_indices + conj_indices)

        words = []
        for n in indices:
            if n != index:
                word = engine.analyze(relations, n, context + [index])
            else:
                word = relations[index].word

            if isinstance(word, str):
                words.append(word)
            elif isinstance(word, list):
                words += word

        this_number = ' '.join(words)

        # Process quantmods
        quantmod_indices = Relation.get_children_with_dep('quantmod',
                                                          relations, index)
        for q in quantmod_indices:
            engine.analyze(relations, q, context + [index],
                           {'num': this_number})

        return this_number


class QuantmodRuleset(Ruleset):

    """A ruleset that processes the 'quantmod' relation."""

    rel = 'quantmod'

    def extract(self, relations, index, context, engine, info):
        """extract(relations, index, context, engine, info) -> None

        Quantifier phrase modifiers always generate propositions.

        Examples:

            * About 100
                quantmod(100, about)
                -> emit((100, about))
        """
        engine.emit((info['num'], relations[index].word))