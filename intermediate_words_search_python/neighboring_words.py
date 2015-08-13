# imports from solution
from utils import string_partitions
from trie_utils import make_trie, trie_contains_word, trie_items, trie_keys


# 3rd-party imports
from itertools import chain


def neighboring_words_fn_factory(dictionary_filename):
    trie = make_trie(dictionary_filename)

    def neighboring_words(string):
        return chain(neighbors_by_transformation(trie, string),
                     neighbors_by_subtraction(trie, string),
                     neighbors_by_addition(trie, string))

    return neighboring_words


def neighbors_by_transformation(trie, string):
    t = trie

    for prefix,char,suffix in string_partitions(string):
        # t is the trie under prefix when each loop starts

        for char2,sub_trie in trie_items(t):  # all peers of char and their sub-tries
            if char2 != char and trie_contains_word(sub_trie, suffix):
                yield prefix + char2 + suffix

        t  = t[char]


def neighbors_by_subtraction(trie, string):
    subtractions = (prefix + suffix for prefix,_,suffix in string_partitions(string))

    for sub in subtractions:
        if trie_contains_word(trie, sub):
            yield sub


def neighbors_by_addition(trie, string):
    t = trie

    for prefix,char,suffix in string_partitions(string):
        # t is the trie under prefix when each loop starts

        for additional_char,sub_trie in trie_items(t):  # all peers of char and their sub-tries
            new_suffix = char + suffix
            if trie_contains_word(sub_trie, new_suffix):
                yield prefix + additional_char + new_suffix

        t  = t[char]

    # and now add one on to the end; t is now sub_trie below string
    for additional_char in trie_keys(t):
        if trie_contains_word(t, additional_char):
            yield string + additional_char
