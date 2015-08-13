# imports from solution
from main  import solution
from utils import show_path


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
    print tests()
