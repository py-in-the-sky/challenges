# imports from solution
from main  import solution, LOCAL_DICTIONARY
from utils import show_path
from time  import time


TEST_CASES = (
    # start word, target word, minimal path length
    ( 'cat',       'dog',      4    ),
    ( 'cat',       'mistrial', 9    ),
    ( 'strong',    'weak',     7    ),
    ( 'hot',       'cold',     4    ),
    ( 'up',        'down',     5    ),
    ( 'left',      'right',    7    ),
    ( 'light',     'heavy',    10   ),
    ( 'computer',  'virus',    12   ),
    ( 'strike',    'freeze',   6    ),
    ( 'fan',       'for',      3    ),
    ( 'duck',      'dusty',    4    ),
    ( 'rue',       'be',       3    ),
    ( 'rue',       'defuse',   5    ),
    ( 'rue',       'bend',     5    ),
    ( 'zoologist', 'zoology',  None )  # no path; these two words are disjoint
)


def tests2():
    t0 = time()
    opts = { 'search_method': 'A*', 'dictionary_filename': LOCAL_DICTIONARY }

    for start_word,target_word,path_len in TEST_CASES:
        path = solution(start_word, target_word, opts)
        assert (len(path) if path else None) == path_len

    return 'tests pass in {} seconds!'.format(time() - t0)



def tests():
    for search_method in ('BFS', 'A*'):
        opts = { 'search_method': search_method }

        assert solution('cat', 'dog', opts) == ('cat', 'cot', 'dot', 'dog')
        assert solution('cat', 'dot', opts) == ('cat', 'cot', 'dot')
        assert solution('cat', 'cot', opts) == ('cat', 'cot')
        assert solution('cat', 'cat', opts) == ('cat', )

        assert solution('fan', 'for', opts) == ('fan', 'fin', 'fir', 'for')

        assert solution('place', 'places', opts) == ('place', 'places')

        assert solution('duck', 'dusty', opts) == ('duck', 'dusk', 'dust', 'dusty')
        assert solution('duck', 'ducked', opts) is None

        assert solution('rue', 'be', opts) == ('rue', 'run', 'runt', 'bunt', 'bent', 'beet', 'bee', 'be')
        assert solution('rue', 'defuse', opts) == ('rue', 'ruse', 'reuse', 'refuse', 'defuse')

        not_a_word_1 = 'NotAWord'
        assert solution('rue', not_a_word_1, opts) is None

        not_a_word_2 = 'plar'
        assert solution(not_a_word_2, 'play', opts) == (not_a_word_2, 'play')

        not_a_word_3 = 'blah'
        assert solution(not_a_word_3, 'defuse', opts) is None

    return 'tests pass!'


if __name__ == '__main__':
    # print tests()
    print tests2()
