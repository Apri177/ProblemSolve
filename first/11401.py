import sys
input = sys.stdin.readline

MOD = 1000000007

def power(a, b, mod):
    """분할 정복을 이용한 거듭제곱 (a^b mod mod)"""
    result = 1
    a = a % mod
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % mod
        a = (a * a) % mod
        b //= 2
    return result

def binomial_coefficient(n, k):
    """이항 계수 C(n, k) mod MOD 계산"""
    if k == 0 or k == n:
        return 1
    
    # 팩토리얼 배열 생성
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = (fact[i-1] * i) % MOD
    
    # C(n, k) = n! / (k! * (n-k)!)
    # 페르마의 소정리를 이용하여 나눗셈을 곱셈으로 변환
    numerator = fact[n]  # n!
    denominator = (fact[k] * fact[n-k]) % MOD  # k! * (n-k)!
    
    # denominator의 모듈로 역원 계산: denominator^(MOD-2)
    inv_denominator = power(denominator, MOD - 2, MOD)
    
    return (numerator * inv_denominator) % MOD

# 입력 받기
N, K = map(int, input().split())

# 결과 출력
print(binomial_coefficient(N, K))

