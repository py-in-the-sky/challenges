class ZigZag:
    def longestZigZag(self, sequence):
        """https://arena.topcoder.com/#/u/practiceCode/1239/1209/1259/1/1239
        https://community.topcoder.com/stat?c=problem_statement&pm=1259&rd=4493

        This is a GREEDY ALGORITHM solution. It's greedy in the sense that the latest
        element is always taken as the last element of the zigzag subsequence. If the
        latest element moves in the same direction as the last step, it's greedily
        used to replace the current last element as a more extreme value in that direction,
        so that the chance that a subsequent element is in the other direction is higher.
        If the latest element moves in the other direction, it's greedily taken to extend
        the zigzag subsequence.
        """
        if len(sequence) <= 1:
            return len(sequence)

        up, down, neutral = 1, -1, 0
        delta, n_elems, last_elem = neutral, 1, sequence[0]

        for i in xrange(1, len(sequence)):
            val = sequence[i]

            if last_elem < val and delta != up:
                n_elems += 1
                delta = up

            elif last_elem > val and delta != down:
                n_elems += 1
                delta = down

            last_elem = val

        return n_elems

    def longestZigZagDP(self, sequence):
        """
        Translated from the C++ at:
        http://www.geeksforgeeks.org/longest-zig-zag-subsequence/
        """
        N = len(sequence)
        A = [[1]*N, [1]*N]
        result = 1

        for i in xrange(1, N):
            for j in xrange(i):
                if sequence[j] < sequence[i] and A[0][i] < A[1][j] + 1:
                    A[0][i] = A[1][j] + 1
                if sequence[j] > sequence[i] and A[1][i] < A[0][j] + 1:
                    A[1][i] = A[0][j] + 1

            result = max(result, A[0][i], A[1][i])

        return result

    def tests(self):
        import random as r

        for _ in xrange(100):
            length = r.randint(1, 50)
            sequence = [r.randint(1, 1000) for _ in xrange(length)]
            assert self.longestZigZag(sequence) == self.longestZigZagDP(sequence)

        sequence = [1, 5, 4]
        assert self.longestZigZag(sequence) == self.longestZigZagDP(sequence)
        sequence = [1, 4, 5]
        assert self.longestZigZag(sequence) == self.longestZigZagDP(sequence)
        sequence = [10, 22, 9, 33, 49, 50, 31, 60]
        assert self.longestZigZag(sequence) == self.longestZigZagDP(sequence)

        sequence = [1, 7, 4, 9, 2, 5]
        assert self.longestZigZag(sequence) == self.longestZigZagDP(sequence) == 6
        sequence = [1, 17, 5, 10, 13, 15, 10, 5, 16, 8]
        assert self.longestZigZag(sequence) == self.longestZigZagDP(sequence) == 7
        sequence = [44]
        assert self.longestZigZag(sequence) == self.longestZigZagDP(sequence) == 1
        sequence = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert self.longestZigZag(sequence) == self.longestZigZagDP(sequence) == 2
        sequence = [70, 55, 13, 2, 99, 2, 80, 80, 80, 80, 100, 19, 7, 5, 5, 5, 1000, 32, 32]
        assert self.longestZigZag(sequence) == self.longestZigZagDP(sequence) == 8
        sequence = [374, 40, 854, 203, 203, 156, 362, 279, 812, 955,
                    600, 947, 978, 46, 100, 953, 670, 862, 568, 188,
                    67, 669, 810, 704, 52, 861, 49, 640, 370, 908,
                    477, 245, 413, 109, 659, 401, 483, 308, 609, 120,
                    249, 22, 176, 279, 23, 22, 617, 462, 459, 244]
        assert self.longestZigZag(sequence) == self.longestZigZagDP(sequence) == 36

        print 'ZigZag tests pass!'
