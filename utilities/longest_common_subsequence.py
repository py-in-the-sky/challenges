from memo import memo


def longest_common_subsequence(a, b):
    "Return lexicographically largest longest common subsequence."

    @memo
    def _loop(i, j):
        if i >= len(a) or j >= len(b):
            return ()

        lcs = _loop(i+1, j)

        for j2 in xrange(j, len(b)):
            if a[i] == b[j2]:
                lcs_candidate = (a[i],) + _loop(i+1, j2+1)
                lcs = max(lcs, lcs_candidate, key=_sequence_order_key)

        return lcs

    def _sequence_order_key(seq):
        "Longer sequence wins.  Ties go to the lexicographically larger sequence."
        return (len(seq), seq)

    return _loop(0, 0)


def longest_common_subsequence_alt(a, b):
    table = {(i, j): 0 for i in xrange(len(a)) for j in xrange(len(b))}

    for i in xrange(len(a)):
        match = 0
        for j in xrange(len(b)):
            match = match or int(a[i] == b[i])
            value_above = table[(i-1, j)] if i > 0 else 0
            table[(i, j)] = match + value_above

    pass
