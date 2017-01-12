"""
https://codility.com/programmers/task/max_slice_sum/

When looking at A[i], there are only two slice sums one has to look at
to find the largest slice sum that ends at index i: A[i] and
(A[i] + the largest slice sum that ends at i-1).  Calculate the largest
slice sum that ends at i for every index in A, and then return the largest
of these sums.
"""


def solution(A):
    largest_sum = largest_sum_ending_at_i = A[0]
    
    for i in xrange(1, len(A)):
        largest_sum_ending_at_i = max(0, largest_sum_ending_at_i) + A[i]
        largest_sum = max(largest_sum, largest_sum_ending_at_i)
    
    return largest_sum
