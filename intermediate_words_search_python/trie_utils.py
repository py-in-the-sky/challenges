# imports from solution
from utils import memo, read_dictionary


# 3rd-party imports
from collections import defaultdict


WORD_END_TOKEN = None


def tree(): return defaultdict(tree)


@memo
def make_trie(dictionary_filename):
    words = read_dictionary(dictionary_filename)
    return reduce(trie_put, words, tree())


def trie_put(trie, word):
    end_trie = reduce(lambda trie, char: trie[char], word, trie)
    end_trie[WORD_END_TOKEN] = WORD_END_TOKEN
    return trie


def trie_get(trie, word):
    "return trie under word if word in trie; otherwise, return None"
    def _get_sub_trie(trie, char):
        return trie[char] if (trie and trie.has_key(char)) else None

    maybe_end_trie = reduce(_get_sub_trie, word, trie)
    return maybe_end_trie


def trie_contains_word(trie, word):
    maybe_end_trie = trie_get(trie, word)
    return maybe_end_trie is not None and maybe_end_trie.has_key(WORD_END_TOKEN)


def trie_items(trie):
    return ((key,value) for key,value in trie.iteritems() if key is not WORD_END_TOKEN)


def trie_keys(trie):
    return (key for key,_ in trie_items(trie))
