"""
Given a string, generate all palindromes possible from its characters.  In other
words, for a given string, find all palindromes among the anagrams of the string.
"""


from collections import Counter


def palindromes(string):
    # Validations and data preparations.
    #   * Find whether there's an odd-multiplicity character that should always appear in the middle of
    #     a palindrome.
    #   * Also construct `half_string`, a string that contains each character that has even multiplicity
    #     in `string`.  Each of these characters appears in `half_string` with its multiplicity halved.
    #     Order doesn't matter.
    character_counts = Counter(string)
    odd_characters = [char for char,count in character_counts.iteritems() if count % 2 == 1]

    if len(odd_characters) > 1:
        return None

    odd = ''
    if odd_characters:
        odd = odd_characters[0]
        character_counts[odd] -= 1

    half_string = ''.join(char * (count / 2) for char,count in character_counts.iteritems())

    # Work on `half_string`.
    return sorted(set(perm + odd + perm[::-1] for perm in permutations(half_string)))


def permutations(string):
    if not string:
        return ['']

    return [char + perm
            for i,char in enumerate(string)
            for perm in permutations(string[:i] + string[i+1:])]


def tests():
    assert palindromes('') == ['']
    assert palindromes('a') == ['a']
    assert palindromes('ab') is None
    assert palindromes('abb') == ['bab']
    assert palindromes('abbcc') == ['bcacb', 'cbabc']
    assert palindromes('aabbcc') == ['abccba', 'acbbca', 'baccab', 'bcaacb', 'cabbac', 'cbaabc']
    assert palindromes('aaabbcc') == ['abcacba', 'acbabca', 'bacacab', 'bcaaacb', 'cababac', 'cbaaabc']
    assert palindromes('racecar') == ['acrerca', 'arcecra', 'carerac', 'craearc', 'racecar', 'rcaeacr']

    print 'tests pass!'


if __name__ == '__main__':
    tests()
