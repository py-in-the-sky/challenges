"""
https://codility.com/programmers/task/equi_leader/
"""


from collections import Counter, defaultdict


def solution(A):
    def _is_equi_leader(i):
        prefix_count_top = running_counts[top]
        suffix_count_top = total_counts[top] - prefix_count_top
        return (prefix_count_top * 2 > i + 1) and (suffix_count_top * 2 > len(A) - i - 1)
    
    total_counts = Counter(A)
    running_counts = defaultdict(int)
    top = A[0]
    result = 0
    
    for i in xrange(len(A) - 1):
        n = A[i]
        running_counts[n] += 1
        top = top if running_counts[top] >= running_counts[n] else n
        
        if _is_equi_leader(i):
            result += 1
            
    return result
