"""
I18N is an abbreviation for 'internationalization', which begins with 'i', ends
with 'n', and has 18 other letters in between.  Find all ways to condense any number
non-contiguous substrings in 'internationalization' or any other string.  E.g., for
'internationalization', return:

i18n
in17n
...
inter3ion2iza3n
...


Loop invariant: at any level in _condense, a prefix has been formed by previous calls.
This prefix is a partial result, and it always ends in a letter and is composed of
integers and letters with no two integers being neighbors.

Therefore, returning a suffix that starts with an integer or letter and has no neighboring
integers will ensure an overall result that has no neighboring integers.
"""


def condense(word):
    if len(word) <= 3:
        return [word]

    first, last, rest = word[0], word[-1], word[1:-1]
    return [first + mid + last for mid in _condense(rest)]


def _condense(word):
    if not word:
        return ['']

    condense_whole_word = [str(len(word))]
    keep_first_char = ['{}{}'.format(word[0], rest) for rest in _condense(word[1:])]
    condense_all_prefixes = ['{}{}{}'.format(str(i), word[i], rest)
                             for i in xrange(1, len(word))
                             for rest in _condense(word[i+1:])]
    # more accurately: condense all proper prefixes (a prefix that's not the whole word)
    return condense_whole_word + keep_first_char + condense_all_prefixes


def tests():
    assert condense('zzz') == ['zzz']
    assert sorted(condense('zaaaz')) == sorted(['z3z', 'za2z', 'z1a1z', 'z2az', 'zaa1z', 'za1az', 'z1aaz', 'zaaaz'])
    # assert 'inter3ion2iza3n' in condense('internationalization')
    # commented out test passes but is long-running

    print 'tests pass!'


if __name__ == '__main__':
    tests()
