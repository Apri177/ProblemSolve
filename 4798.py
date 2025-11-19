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

def segmented_sieve(a, b, L, U, is_prime_sieve, primes):
    if U < L:
        return 0
    
    size = U - L + 1
    is_composite = [False] * size
    
    if math.gcd(a, b) > 1:
        if L == 0 and b > 2:
            if b < len(is_prime_sieve):
                if is_prime_sieve[b]:
                    return 1
            elif miller_rabin(b):
                return 1
        return 0
    
    values = []
    for n in range(L, U + 1):
        t_n = a * n + b
        values.append(t_n)
        if t_n < 2:
            is_composite[n - L] = True
    
    if not values:
        return 0
    
    max_value = max(values)
    sqrt_max = int(math.isqrt(max_value)) + 1
    
    for p in primes:
        if p > sqrt_max:
            break
        if a % p == 0:
            continue
        
        if math.gcd(a, p) == 1:
            a_inv = mod_inverse(a, p)
            if a_inv is None:
                continue
            n = ((-b % p) * a_inv) % p
            if n < L:
                n += ((L - n + p - 1) // p) * p
        else:
            if b % p == 0:
                n = L
            else:
                continue
        
        if n > U:
            continue
            
        start = n
        while start <= U:
            idx = start - L
            if idx >= 0 and idx < size:
                t_n = values[idx]
                if t_n >= p * p:
                    is_composite[idx] = True
            start += p
    
    count = 0
    for i in range(size):
        if is_composite[i]:
            continue
        
        t_n = values[i]
        
        if t_n < 2:
            continue
        
        if t_n < len(is_prime_sieve):
            if is_prime_sieve[t_n]:
                count += 1
            continue
        
        sqrt_tn = int(math.isqrt(t_n))
        is_prime = True
        for p in primes:
            if p > sqrt_tn:
                break
            if t_n % p == 0:
                is_prime = False
                break
        
        if is_prime:
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
        
        count = segmented_sieve(a, b, L, U, is_prime_sieve, primes)
        print(f"Case {test_case_num}: {count}")
    except:
        break
