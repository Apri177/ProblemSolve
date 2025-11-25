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
    
    is_sieved_small = [False] * q
    primes = []
    for i in range(2, q):
        if not is_sieved_small[i]:
            primes.append(i)
            for j in range(i * i, q, i):
                is_sieved_small[j] = True
    
    rs = [False] * range_len
    
    for i in primes:
        if a % i == 0:
            continue
        
        n_mod = EEA(a, i, b)
        st = (L // i) * i + n_mod
        if st < L:
            st += i
        
        for n in range(st, U + 1, i):
            value = n * a + b
            
            if value != i:
                rs[n - L] = True
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