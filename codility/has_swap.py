def has_swap(A, B):
    "Is there one exchange between A and B that'll make their sums equal?"
    # https://codility.com/media/train/2-CountingElements.pdf
    # assert len(A) == len(B)
    # assert all(type(a) == int for a in A)
    # assert all(type(b) == int for b in B)

    sum_A = sum(A)
    sum_B = sum(B)
    diff = sum_A - sum_B

    if diff % 2 == 1:
        return False

    set_A = set(A)
    # The exchange should change sum(A) by -(diff / 2)
    # So the exchange should be: B[j] - A[i] = -(diff / 2),
    # making the complement of B[j] be A[i] = B[j] + diff / 2.
    complement = lambda b: b + diff / 2
    return any((complement(b) in set_A) for b in B)
