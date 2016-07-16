"""
https://code.google.com/codejam/contest/90101/dashboard#s=p2
"""


from collections import defaultdict


PHRASE = 'welcome to code jam'
MOD = 10000


def characters_and_suffixes(phrase=PHRASE):
    if phrase:
        yield phrase[-1], ''
        for i in xrange(1, len(phrase)):
            yield phrase[-(i+1)], phrase[-i:]


def make_tables(phrase=PHRASE):
    counts = {'': 1}
    suffixes = defaultdict(list)

    for char,suffix in characters_and_suffixes(phrase):
        suffixes[char].append(suffix)
        counts[char + suffix] = 0

    for char,suffs in suffixes.iteritems():
        suffixes[char] = tuple(suffs)

    return counts, suffixes


def welcome_to_code_jam(text, phrase=PHRASE):
    counts, suffixes = make_tables(phrase)

    for char in reversed(text.lower()):
        for suffix in suffixes[char]:
            suffix2 = char + suffix
            counts[suffix2] = (counts[suffix2] + counts[suffix]) % MOD

    count = str(counts[phrase])
    return '0' * (4-len(count)) + count


def main():
    T = int(raw_input())
    for t in xrange(1, T+1):
        print 'Case #{}: {}'.format(t, welcome_to_code_jam(raw_input()))


if __name__ == '__main__':
    main()
