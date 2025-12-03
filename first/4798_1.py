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

MAX_SIEVE = 10**6 + 1
is_sieved_small = [False] * MAX_SIEVE
primes = []

def generate_primes():
    global primes
    if primes: 
        return
    
    for i in range(2, MAX_SIEVE):
        if not is_sieved_small[i]:
            primes.append(i)
            for j in range(i * i, MAX_SIEVE, i):
                is_sieved_small[j] = True

def sieve(a: int, b: int, L: int, U: int) -> int:
    if L > U: return 0
    max_value = U * a + b
    range_len = U - L + 1
    
    if math.gcd(a, b) > 1:
        g = math.gcd(a, b)
        if g >= MAX_SIEVE or is_sieved_small[g]:
            return 0
    
        if (g - b) % a == 0:
            n = (g - b) // a
            if L <= n <= U:
                return 1
        return 0
    
    sqrt_max = math.isqrt(max_value) + 1
    
    rs = [False] * range_len
    
    for p in primes:
        if p > sqrt_max:
            break
        if a % p == 0:
            continue
        
        n_mod = EEA(a, p, b)
        if n_mod == -1:
            continue
        
        L_mod = L % p
        if n_mod >= L_mod:
            st = L + (n_mod - L_mod)
        else:
            st = L + (n_mod - L_mod + p)
        
        idx = st - L
        while idx < range_len:
            val = (L + idx) * a + b
            if val != p:
                rs[idx] = True
            idx += p
    count = 0
    for i in range(range_len):
        n = L + i
        value = n * a + b
        
        if value <= 1:
            continue
        if not rs[i]:
            count += 1
    
    return count

if __name__ == "__main__":
    generate_primes()
    
    test_case_num = 0
    
    while True:
        line = input()
        if line.strip() == "0":
            break
        
        a, b, L, U = map(int, line.split())
        test_case_num += 1
        
        count = sieve(a, b, L, U)
        print(f"Case {test_case_num}: {count}")