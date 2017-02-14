class BadNeighbors:
    def maxDonations(self, donations):
        """https://community.topcoder.com/stat?c=problem_statement&pm=2402&rd=5009

        A DYNAMIC PROGRAMMING solution.
        """
        N = len(donations)

        if N == 2:
            return max(donations)

        return max(self._max_donations(donations, 0, N-1), self._max_donations(donations, 1, N))

    def _max_donations(self, donations, lo, hi):
        s2 = donations[lo]
        s1 = max(s2, donations[lo+1])

        for i in xrange(lo+2, hi):
            temp = max(s1, s2 + donations[i])
            s1, s2 = temp, s1

        return s1
