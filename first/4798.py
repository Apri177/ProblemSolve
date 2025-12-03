import sys
import math

def sieve(max_num):
    is_prime = [True] * (max_num + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(math.isqrt(max_num)) + 1):
        if is_prime[i]:
            for j in range(i * i, max_num + 1, i):
                is_prime[j] = False
    
    primes = []
    for i in range(2, max_num + 1):
        if is_prime[i]:
            primes.append(i)
    return is_prime, primes

def power(n, k, mod):
    result = 1
    while k:
        if k & 1:
            result = (result * n) % mod
        n = (n * n) % mod
        k >>= 1
    return result

def miller_rabin(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small_primes:
        if n % p == 0:
            return n == p
    
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    if n < 2047:
        test_primes = [2]
    elif n < 1373653:
        test_primes = [2, 3]
    elif n < 25326001:
        test_primes = [2, 3, 5]
    elif n < 3215031751:
        test_primes = [2, 3, 5, 7]
    elif n < 2152302898747:
        test_primes = [2, 3, 5, 7, 11]
    elif n < 3474749660383:
        test_primes = [2, 3, 5, 7, 11, 13]
    elif n < 341550071728321:
        test_primes = [2, 3, 5, 7, 11, 13, 17]
    else:
        test_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    
    for a in test_primes:
        if a >= n:
            break
        x = power(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

def is_prime_number(n, is_prime_sieve, primes):
    """주어진 수가 소수인지 판별"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # 작은 수는 에라토스테네스의 체로 판별
    if n < len(is_prime_sieve):
        return is_prime_sieve[n]
    
    # 큰 수는 Miller-Rabin으로 판별
    if n < 10**12:
        return miller_rabin(n)
    
    # 매우 큰 수는 trial division으로 판별
    sqrt_n = int(math.isqrt(n))
    for p in primes:
        if p > sqrt_n:
            break
        if n % p == 0:
            return False
    return True

def count_primes_in_arithmetic_sequence(a, b, L, U, is_prime_sieve, primes):
    """등차수열 t(n) = a*n + b에서 L ≤ n ≤ U 범위의 소수 개수를 구함 (Segmented Sieve 사용)"""
    if U < L:
        return 0
    
    # a와 b의 최대공약수 확인
    g = math.gcd(a, b)
    
    # a와 b가 서로소가 아닌 경우
    if g > 1:
        # 등차수열의 모든 항이 g의 배수이므로, g가 소수가 아니면 소수가 없음
        if not is_prime_number(g, is_prime_sieve, primes):
            return 0
        
        # g가 소수인 경우, t(n) = a*n + b = g * (a/g * n + b/g)
        # t(n)이 소수가 되려면 g * (a/g * n + b/g) = g여야 함
        # 즉, a/g * n + b/g = 1이어야 함
        # 하지만 더 간단하게: b = g이고 n = 0일 때만 t(0) = b = g가 소수
        if b == g and L <= 0 <= U:
            return 1
        return 0
    
    # Segmented Sieve 사용
    size = U - L + 1
    is_composite = [False] * size
    
    # 범위의 최소값과 최대값
    min_val = a * L + b
    max_val = a * U + b
    
    # 2보다 작은 수는 소수가 아님
    for i in range(size):
        n = L + i
        t_n = a * n + b
        if t_n < 2:
            is_composite[i] = True
    
    # 최대값의 제곱근까지의 소수로 체를 걸러냄
    sqrt_max = int(math.isqrt(max_val))
    
    for p in primes:
        if p > sqrt_max:
            break
        
        # a*n + b ≡ 0 (mod p)인 n을 찾음
        # a*n ≡ -b (mod p)
        if a % p == 0:
            # a가 p의 배수인 경우
            if b % p == 0:
                # b도 p의 배수면 모든 항이 p의 배수
                # 하지만 a와 b가 서로소이므로 이 경우는 발생하지 않음
                continue
            else:
                # a는 p의 배수지만 b는 아니면 소수 없음
                continue
        else:
            # a와 p가 서로소이므로 역원 존재
            a_inv = mod_inverse(a, p)
            if a_inv is None:
                continue
            
            # n ≡ (-b) * a^(-1) (mod p)
            n0 = ((-b % p) * a_inv) % p
            
            # L <= n <= U 범위에서 n0 + k*p 형태의 n을 찾음
            # n0는 0 <= n0 < p 범위에 있으므로, L보다 작으면 조정 필요
            if n0 < L:
                n0 += ((L - n0 + p - 1) // p) * p
            elif n0 > U:
                # n0가 범위를 벗어나면 이 소수로는 걸러낼 수 없음
                continue
            
            # n0부터 시작해서 p씩 증가하며 체로 걸러냄
            n = n0
            while n <= U:
                idx = n - L
                if idx >= 0 and idx < size:
                    t_n = a * n + b
                    # p^2 이상인 경우만 체로 걸러냄 (p 자체는 소수이므로)
                    # t_n == p인 경우도 소수이므로 걸러내면 안 됨
                    if t_n > p and t_n >= p * p:
                        is_composite[idx] = True
                n += p
    
    # 소수 개수 세기
    count = 0
    for i in range(size):
        if not is_composite[i]:
            n = L + i
            t_n = a * n + b
            if t_n >= 2:
                # 작은 수는 이미 체로 확인됨
                if t_n < len(is_prime_sieve):
                    if is_prime_sieve[t_n]:
                        count += 1
                else:
                    # 큰 수는 추가 확인 필요 (하지만 대부분 이미 체로 걸러짐)
                    # 체로 걸러지지 않은 수는 소수일 가능성이 높음
                    # Miller-Rabin으로 최종 확인
                    if miller_rabin(t_n):
                        count += 1
    
    return count

max_sieve = 10**6
is_prime_sieve, primes = sieve(max_sieve)

test_case_num = 0

while True:
    try:
        line = input()
        if line == "0":
            break
        
        a, b, L, U = map(int, line.split())
        test_case_num += 1
        
        count = count_primes_in_arithmetic_sequence(a, b, L, U, is_prime_sieve, primes)
        print(f"Case {test_case_num}: {count}")
    except:
        break
