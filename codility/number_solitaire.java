// https://codility.com/programmers/lessons/17-dynamic_programming/number_solitaire/


import java.util.*;


class Solution {
    public int solution(int[] A) {
        HashMap<Integer, Integer> memo = new HashMap<Integer, Integer>();
        memo.put(A.length - 1, A[A.length - 1]);
        
        for (int i = A.length - 2; i >= 0; i--) {
            int max_from_i = memo.get(i + 1);
            
            for (int j = i + 2; j < A.length && j <= i + 6; j++) {
                int max_from_j = memo.get(j);
                max_from_i = max_from_j > max_from_i ? max_from_j : max_from_i;
            }
            
            memo.put(i, max_from_i + A[i]);
        }
        
        return memo.get(0);
    }
}
