"""
https://codility.com/programmers/task/max_counters/


Proof of O(N+M) runtime:
As you iterate over A, every time you encounter a INCREASE operation,
you have to do O(1) work to update `counts`.  Let's say you iterate
over P elements of A before encountering the MAX operation.  You've
done P work so far, and by the lemma below, you do P work to derive
the new baseline.  So after iterating over P elements, you've done
O(P) work.  You can show by induction on iterations that after iterating
on all M elements, you've done O(M) work.  And then finally you construct
the counters at the end before returning them, which takes O(N) work.  So
in the end you've done O(N+M) work.

(In the above argument, the analysis of O(P) has the flavor of amortized analysis.)

Lemma: calculating `baseline` takes O(P), where P is the number of elements
you've iterated over since you last performed the MAX operation.

Proof of lemma:
After P INCREASE operations, you have at most P elements in `counts`.  To
increase `baseline`, you must extract the max from `counts`, which takes
O(P) work.  (`counts.clear()` also take O(P) work.)


Why not just keep an N-sized array of counters throughout?  Because
each time you come across the MAX operation, you'd have to do O(N) work.
If all M items in A (or, say, every other) indicate the MAX operation,
then the algorithm would run in O(M*N) time.
"""


from collections import defaultdict


def solution(N, A):
    baseline = 0
    counts = defaultdict(int)
    for n in A:
        if n == N+1 and len(counts) > 0:
            baseline += max(counts.itervalues())
            counts.clear()
        elif n < N+1:
            counts[n] += 1
        
    result = [baseline] * N
    for i,ct in counts.iteritems():
        result[i-1] += ct
    return result
