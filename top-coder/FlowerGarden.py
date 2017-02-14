class FlowerGarden:
    "https://community.topcoder.com/stat?c=problem_statement&pm=1918&rd=5006"
    def getOrdering(self, height, bloom, wilt):
        """
        This is a GREEDY ALGORITHM and SORTING solution.

        The greedy element: first sort all flowers by height ascending.

        The sorting element: the sorting condition is two-fold:

            1. We want taller flowers closer to the front, so I will keep bubbling
               forward since any flower inserted ahead of me is smaller than me.
            2. We want any two flowers in bloom at the same to both be visible (i.e., both
               be sorted in ascending order according to height), so I will bubble forward
               until I meet a flower whose bloom time mine overlaps with.

        Implement a MODIFIED BUBBLE SORT to take care of this second sorting step.

        By first sorting by height ascending, we ensure that when a flower is
        bubble-sorted in, all flowers inserted  in row before it are smaller than it.
        Therefore, when it stops bubbling up in row (i.e., when it meets the first flower
        whose bloom time it overlaps with) we know that all flowers ahead of it whose
        bloom time it overlaps with are smaller than itself.

        Therefore, given the initial greedy step, by bubbling the flower forward, we
        ensure sorting goal 1 is fulfilled; by stopping at the first overlap, we ensure
        sorting goal 2 is fulfilled.

        Note how we express the two sorting conditions as simply as possible in order to
        clarify the minimal amount of dependency between the flower being inserted in the
        row and the flowers already in the row. Specifically, the second sorting condition
        is expressed just in terms of two flowers: the flower being inserted and the flower
        being compared to it. Then from the greedy preprocessing step, we can derive that
        the second sorting step is satisfied for all flowers ahead of it with whom it may
        have an overlaping bloom time. And from the greedy preprocessing step, we can
        satisfy the first sorting condition easily as well, by moving the inserted flower
        as far forward as we can without violating the second sorting condition. By using
        the modified bubble sort, we're guaranteed to catch the furthest right flower that
        is smaller than the flower being inserted and that has an overlapping bloom time with
        it.

        References:
        http://stackoverflow.com/questions/11248764/how-is-the-flowergarden-pr0blem-on-topcoder-a-dp-one
        https://apps.topcoder.com/forums/?module=Thread&threadID=655393
        http://www.topcoder.com/tc?module=Static&d1=match_editorials&d2=tccc04_online_rd_1
        """
        flowers = sorted(zip(height, bloom, wilt))
        row = []

        for i in xrange(len(flowers)):
            row.append(flowers[i])

            for j in reversed(xrange(1, len(row))):
                if self.overlapped(row[j], row[j-1]):
                    break
                else:
                    row[j], row[j-1] = row[j-1], row[j]

        return [flower[0] for flower in row]

    def overlapped(self, flower1, flower2):
        _, bloom1, wilt1 = flower1
        _, bloom2, wilt2 = flower2
        return not (wilt2 < bloom1 or wilt1 < bloom2)

    def tests(self):
        h, b, w = [5,4,3,2,1], [1,1,1,1,1], [365,365,365,365,365]
        assert self.getOrdering(h, b, w) == [1,  2,  3,  4,  5]
        h, b, w = [5,4,3,2,1], [1,5,10,15,20], [4,9,14,19,24]
        assert self.getOrdering(h, b, w) == [5,  4,  3,  2,  1]
        h, b, w = [5,4,3,2,1], [1,5,10,15,20], [5,10,15,20,25]
        assert self.getOrdering(h, b, w) == [1,  2,  3,  4,  5]
        h, b, w = [5,4,3,2,1], [1,5,10,15,20], [5,10,14,20,25]
        assert self.getOrdering(h, b, w) == [3,  4,  5,  1,  2]
        h, b, w = [1,2,3,4,5,6], [1,3,1,3,1,3], [2,4,2,4,2,4]
        assert self.getOrdering(h, b, w) == [2,  4,  6,  1,  3,  5]
        h, b, w = [3,2,5,4], [1,2,11,10], [4,3,12,13]
        assert self.getOrdering(h, b, w) == [4,  5,  2,  3]

        print 'FlowerGarden tests pass!'
