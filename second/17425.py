# import sys
# input = sys.stdin.readline
#
# for _ in range(int(input())):
#     print(int(input()))

"""
문제: 테스트 케이스가 여러 개 주어질 때 약수의 합을 빠르게 구하기

시간 복잡도 분석:
- 테스트 케이스 T개, 각 N ≤ 1,000,000
- 매번 O(N) 계산하면: O(T × N) → 시간 초과!

해결책: 전처리 + 누적합
1. 미리 모든 값을 계산해두기 (전처리)
2. 각 쿼리를 O(1)에 답하기

전처리 과정:
- f(n) = n의 약수의 합
- g(n) = Σf(i) for i=1 to n (1부터 n까지 약수의 합)
"""

import sys
input = sys.stdin.readline

# 최대값 설정
MAX_N = 1000000

# 1단계: 각 수의 약수의 합 구하기
# divisor_sum[i] = i의 약수의 합
divisor_sum = [0] * (MAX_N + 1)

# 효율적인 방법: 각 수 i가 어떤 수들의 약수가 되는지 계산
for i in range(1, MAX_N + 1):
    # i는 i, 2i, 3i, ..., ki (ki ≤ MAX_N)의 약수
    for j in range(i, MAX_N + 1, i):
        divisor_sum[j] += i

# 예시:
# i=1: 1,2,3,4,5,... 모든 수에 1 더하기
# i=2: 2,4,6,8,... 모든 짝수에 2 더하기
# i=3: 3,6,9,12,... 3의 배수에 3 더하기

# 2단계: 누적합 구하기
# cumulative_sum[n] = Σ divisor_sum[i] for i=1 to n
cumulative_sum = [0] * (MAX_N + 1)
for i in range(1, MAX_N + 1):
    cumulative_sum[i] = cumulative_sum[i-1] + divisor_sum[i]

# 3단계: 각 쿼리에 O(1)로 답하기
T = int(input())
for _ in range(T):
    n = int(input())
    print(cumulative_sum[n])
