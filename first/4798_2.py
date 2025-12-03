import math
import sys

input = sys.stdin.readline

# 재귀 깊이 설정 (큰 수 연산 시 필요할 수 있음)
sys.setrecursionlimit(2000)

# =========================================================
# 1. 수학적 헬퍼 함수
# =========================================================

# 확장 유클리드 호제법 (ax + by = gcd(a, b))
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (g, x, y)

# 선형 합동식 해: ax ≡ -b (mod p)의 시작값 n_mod를 구함
def EEA(a, p, b):
    g, x, y = egcd(a, p)
    
    # gcd(a, p) != 1 이면 역원이 존재하지 않아 이 함수로 해를 찾을 수 없음
    if g != 1:
        return -1 
    
    # x는 a의 모듈러 역원 (a_inv)
    a_inv = x % p
    if a_inv < 0:
        a_inv += p
        
    # n ≡ -b * a_inv (mod p)
    n_mod = (-b * a_inv) % p
    if n_mod < 0:
        n_mod += p
        
    return n_mod

# 밀러-라빈 소수 판별 (최종 검증용)
# 64비트 정수(약 10^18) 범위에서 결정적인(100% 정확한) 테스트
BASES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] 

def is_prime(n):
    if n < 2: return False
    # 작은 소수로 빠르게 검사
    for p in BASES:
        if n == p: return True
        if n % p == 0: return False

    # n-1 = d * 2^s 형태로 분해
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    # 밀러-라빈 테스트
    for a in BASES:
        if a >= n: break
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
            
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
            
    return True

# =========================================================
# 2. 메인 솔버 (Segmented Sieve Logic)
# =========================================================

def solve_optimized_sieve(a: int, b: int, L: int, U: int) -> int:
    """
    등차수열 an + b (L <= n <= U)의 소수 개수를 효율적으로 계산합니다.
    """
    if L > U: return 0
    
    # 0. 전처리 및 상한 설정
    max_val = U * a + b
    q = math.isqrt(max_val) + 1 # Sieve 상한 (<= 10^6 범위)
    range_len = U - L + 1
    
    # 0.1. gcd(a, b) > 1 예외 처리
    if math.gcd(a, b) > 1:
        # 이 경우, L*a+b == gcd(a,b)일 때만 소수 가능성 있음.
        if L * a + b == math.gcd(a, b) and is_prime(L * a + b):
            return 1
        return 0

    # 1. 작은 소수 생성 (q까지의 Sieve of Eratosthenes)
    is_sieved_small = [False] * q
    primes = []
    for i in range(2, q):
        if not is_sieved_small[i]:
            primes.append(i)
            for j in range(i * i, q, i):
                is_sieved_small[j] = True

    # 2. 구간 배열 초기화 (rs 배열 역할: False = 소수 후보, True = 합성수)
    rs = [False] * range_len
    
    # 3. 체 치기 (작은 소수들로 구간 [L, U]를 지움)
    for i in primes: # i는 현재 소수
        
        # 3.1. a가 i의 배수이면 건너뜀 (EEA 조건 불만족)
        if a % i == 0:
            continue
            
        # 3.2. EEA로 시작 위치 (n_mod) 계산
        n_mod = EEA(a, i, b) 
        
        # 3.3. 실제 구간 [L, U] 내의 시작 인덱스 (n=st) 계산
        st = (L // i) * i + n_mod 
        if st < L:
            st += i
            
        # 3.4. 체 치기: n=st부터 U까지 i 간격으로 지움
        for n in range(st, U + 1, i):
            val = n * a + b
            
            # ★ 최적화된 부분: 단순 비교 ★
            # val은 i의 배수임이 보장됨. val == i인 경우만 소수, 아니면 합성수.
            # L이 크기 때문에 val == i일 확률은 극히 낮지만, 원칙상 체크.
            if val != i:
                rs[n - L] = True # 합성수로 표시

    # 4. 최종 카운트 및 밀러-라빈 검증
    prime_count = 0
    for i in range(range_len):
        n = L + i
        val = n * a + b
        
        # 4.1. 1은 소수가 아님 (val이 1이 될 가능성도 체크)
        if val <= 1: 
            continue
        
        # 4.2. 체에 걸러지지 않은 후보들만 밀러-라빈 검증
        if not rs[i]:
            # is_prime(val)은 10^12 범위의 소수를 빠르게 판별 (최종 검증)
            if is_prime(val): 
                prime_count += 1
                
    return prime_count

if __name__ == "__main__":
    test_case_num = 0
    
    while True:
        line = input()
        if line.strip() == "0":
            break
        
        a, b, L, U = map(int, line.split())
        test_case_num += 1
        
        count = solve_optimized_sieve(a, b, L, U)
        print(f"Case {test_case_num}: {count}")
