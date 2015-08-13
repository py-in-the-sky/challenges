# imports from solution
from neighboring_words import neighboring_words_fn_factory
from shortest_path_search import shortest_path_bfs, shortest_path_A_star


LOCAL_DICTIONARY = '/usr/share/dict/words'


SEARCH_METHODS = {
    'BFS': shortest_path_bfs,
    'A*':  shortest_path_A_star
}


def solution(word1, word2, opts={}):
    "return path if word1 and word2 are connected; otherwise, if disjointed, return None"

    search_method        = opts.get('search_method', 'BFS')
    queue                = opts.get('queue', None)
    dictionary_filename  = opts.get('dictionary_filename', None)

    neighboring_words_fn = neighboring_words_fn_factory(dictionary_filename)
    search_fn            = SEARCH_METHODS[search_method]

    return search_fn(word1, word2, neighboring_words_fn, queue)
