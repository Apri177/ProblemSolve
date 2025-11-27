import math
import sys

input = sys.stdin.readline

sys.setrecursionlimit(2000)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (g, x, y)

def EEA(a, p, b):
    """
    확장 유클리드 알고리즘으로 선형 합동식 a*n ≡ -b (mod p)의 해를 구합니다.
    즉, a*n + b ≡ 0 (mod p)인 n ≡ n_mod (mod p)를 반환합니다.
    """
    g, x, y = egcd(a, p)

    if g != 1:
        return -1
    
    a_inverse = x % p
    if a_inverse < 0:
        a_inverse += p
        
    n_mod = (-b * a_inverse) % p
    if n_mod < 0:
        n_mod += p
    
    return n_mod

BASES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

def is_prime(n):
    """Miller-Rabin 소수 판별법 (10^12 범위에서 결정적)"""
    if n < 2: return False
    for p in BASES:
        if n == p: return True
        if n % p == 0: return False
    
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
        
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

def sieve(a: int, b: int, L: int, U: int) -> int:
    if L > U: return 0
    max_value = U * a + b
    q = math.isqrt(max_value) + 1
    range_len = U - L + 1
    
    if math.gcd(a, b) > 1:
        if L * a + b == math.gcd(a, b) and is_prime(L * a + b):
            return 1
        return 0
    
    # 작은 소수 생성
    is_sieved_small = [False] * q
    primes = []
    for i in range(2, q):
        if not is_sieved_small[i]:
            primes.append(i)
            for j in range(i * i, q, i):
                is_sieved_small[j] = True
    
    # 합성수 표시 배열 (False = 소수 후보, True = 합성수)
    rs = [False] * range_len
    
    # ★ 최적화: 작은 소수부터 처리하여 조기 필터링
    # 작은 소수로 먼저 걸러내면 나중에 큰 소수 처리 시 반복 횟수가 줄어듭니다
    
    for p in primes:
        if a % p == 0:
            continue
        
        n_mod = EEA(a, p, b)
        if n_mod == -1:
            continue
        
        # ★ 최적화 1: 시작 위치를 더 효율적으로 계산
        # n ≡ n_mod (mod p)이고 n >= L인 최소 n 찾기
        # L % p를 계산하여 n_mod와 비교
        L_mod = L % p
        if n_mod >= L_mod:
            st = L + (n_mod - L_mod)
        else:
            st = L + (n_mod - L_mod + p)
        
        # ★ 최적화 2: range() 대신 while 루프로 직접 인덱스 업데이트
        # range() 객체 생성 오버헤드 완전 제거
        idx = st - L
        
        # ★ 최적화 3: p^2 이상인 경우만 체로 걸러내기
        # p 자체는 소수이므로, val == p인 경우는 소수로 남겨둠
        # 하지만 L이 크면 val == p일 가능성은 거의 없으므로
        # 대부분의 경우 바로 합성수로 표시 가능
        
        while idx < range_len:
            # 이미 합성수로 표시된 경우 건너뛰기 (선택적 최적화)
            # 하지만 작은 소수부터 처리하므로 대부분 처음 만나는 경우
            
            # val = (L + idx) * a + b는 p의 배수임이 보장됨
            # val == p인 경우만 소수, 나머지는 합성수
            # L이 크면 val == p일 가능성은 거의 없으므로
            # 대부분의 경우 바로 합성수로 표시
            val = (L + idx) * a + b
            
            # p^2 이상인 경우만 합성수로 표시
            # val == p인 경우는 소수이므로 건너뜀
            if val > p and val >= p * p:
                rs[idx] = True
            
            idx += p
    
    # 최종 카운트
    count = 0
    for i in range(range_len):
        n = L + i
        value = n * a + b
        
        if value <= 1:
            continue
        if not rs[i]:
            if is_prime(value):
                count += 1
    
    return count

if __name__ == "__main__":
    test_case_num = 0
    
    while True:
        line = input()
        if line.strip() == "0":
            break
        
        a, b, L, U = map(int, line.split())
        test_case_num += 1
        
        count = sieve(a, b, L, U)
        print(f"Case {test_case_num}: {count}")

