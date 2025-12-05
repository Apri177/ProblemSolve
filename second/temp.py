"""
N보다 작거나 같은 수들의 약수의 합을 구하는 문제

예시: N=5
- 1의 약수: {1} → 합 = 1
- 2의 약수: {1, 2} → 합 = 3
- 3의 약수: {1, 3} → 합 = 4
- 4의 약수: {1, 2, 4} → 합 = 7
- 5의 약수: {1, 5} → 합 = 6
전체 합 = 1 + 3 + 4 + 7 + 6 = 21

핵심 아이디어:
- 각 수 i가 몇 개의 수의 약수가 되는지 생각
- i는 i, 2i, 3i, ..., ki (ki ≤ N)의 약수
- 즉, i는 floor(N/i)개의 수의 약수가 됨
- 따라서 i는 전체 합에 i × floor(N/i)만큼 기여

공식: Σ(i=1 to N) i × floor(N/i)

예시로 확인 (N=5):
- 1: 5개 수의 약수 → 1 × 5 = 5
- 2: 2개 수의 약수 → 2 × 2 = 4
- 3: 1개 수의 약수 → 3 × 1 = 3
- 4: 1개 수의 약수 → 4 × 1 = 4
- 5: 1개 수의 약수 → 5 × 1 = 5
총합: 5 + 4 + 3 + 4 + 5 = 21 ✓
"""

# 방법 1: 직관적인 방법 (느림 - O(N²))
def sum_of_divisors_naive(n):
    """각 수마다 약수를 모두 찾아서 더하기"""
    total = 0
    for num in range(1, n + 1):
        # num의 약수의 합 구하기
        for divisor in range(1, num + 1):
            if num % divisor == 0:
                total += divisor
    return total


# 방법 2: 효율적인 방법 (빠름 - O(N))
def sum_of_divisors_efficient(n):
    """
    각 수 i가 몇 개의 수의 약수가 되는지 계산
    i는 floor(N/i)개의 수의 약수가 됨
    """
    total = 0
    for i in range(1, n + 1):
        # i가 약수로 포함되는 수의 개수
        count = n // i
        # i가 전체 합에 기여하는 양
        total += i * count
    return total


# 메인 코드
if __name__ == "__main__":
    n = int(input())
    
    # N이 작으면 두 방법 모두 가능
    # N이 크면 (예: 1,000,000) 효율적인 방법 사용
    if n <= 10000:
        # 두 방법 비교 가능
        result1 = sum_of_divisors_naive(n)
        result2 = sum_of_divisors_efficient(n)
        print(f"직관적 방법: {result1}")
        print(f"효율적 방법: {result2}")
        print(f"결과: {result2}")
    else:
        # 큰 N에는 효율적인 방법만 사용
        result = sum_of_divisors_efficient(n)
        print(result)

