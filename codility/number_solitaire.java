// https://codility.com/programmers/lessons/17-dynamic_programming/number_solitaire/


class Solution {
    public int solution(int[] A) {
        int N = A.length;
        int[] memo = new int[N];
        memo[N - 1] = A[N - 1];
        
        for (int i = N - 2; i >= 0; i--) {
            int max_i = memo[i + 1];
            
            for (int j = i + 2; j < N && j <= i + 6; j++) {
                int max_j = memo[j];
                max_i = max_j > max_i ? max_j : max_i;
            }
            
            memo[i] = max_i + A[i];
        }
        
        return memo[0];
    }
}
