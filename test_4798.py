import sys
import math
import importlib.util

spec = importlib.util.spec_from_file_location("module_4798", "4798_1.py")
module_4798 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module_4798)

def is_prime_simple(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def count_primes_naive(a, b, L, U):
    count = 0
    for n in range(L, U + 1):
        t_n = a * n + b
        if t_n >= 2 and is_prime_simple(t_n):
            count += 1
    return count

is_prime_sieve = module_4798.sieve
primes = module_4798.is_prime
count_primes = module_4798.count_primes

test_cases = [
    (4, 3, 0, 10),
    (1, 2, 0, 100),
    (1, 0, 2, 100),
    (2, 1, 0, 50),
    (6, 3, 0, 0),
    (6, 3, 1, 10),
    (4, 2, 0, 10),
    (1, 1, 0, 0),
    (1, 1, 1, 1),
    (2, 0, 2, 10),
    (10, 3, 0, 5),
    (1, 2, 0, 0),
    (1, 2, 1, 1),
    (100, 97, 0, 10),
    (1, 999983, 0, 0),
    (1, 2, 0, 1),
    (2, 3, 0, 0),
    (3, 2, 0, 0),
    (1, 0, 0, 0),
    (1, 1, 0, 1),
    (1, 3, 0, 0),
    (2, 1, 0, 0),
    (3, 1, 0, 0),
    (4, 1, 0, 0),
    (5, 1, 0, 0),
    (6, 1, 0, 0),
    (7, 1, 0, 0),
    (8, 1, 0, 0),
    (9, 1, 0, 0),
    (10, 1, 0, 0),
    (1, 2, 0, 1000),
    (2, 1, 0, 1000),
    (3, 2, 0, 1000),
    (4, 3, 0, 1000),
    (10, 7, 0, 1000),
    (100, 97, 0, 100),
    (1000, 997, 0, 100),
    (1, 0, 0, 1000),
    (2, 0, 0, 1000),
    (1, 1, 0, 1000),
    (1, 3, 0, 1000),
    (6, 5, 0, 0),
    (8, 3, 0, 0),
    (10, 3, 0, 0),
    (12, 5, 0, 0),
    (14, 3, 0, 0),
    (15, 2, 0, 0),
    (20, 3, 0, 0),
    (1, 2, 100, 200),
    (1, 2, 1000, 2000),
    (2, 1, 100, 200),
    (3, 2, 100, 200),
]

print("Testing edge cases...")
all_passed = True
failed_cases = []

for a, b, L, U in test_cases:
    if a * U + b > 10**12:
        continue
    if U - L > 10**6:
        continue
    
    try:
        result1 = count_primes(a, b, L, U, is_prime_sieve, primes)
        result2 = count_primes_naive(a, b, L, U)
        
        if result1 != result2:
            print(f"FAIL: a={a}, b={b}, L={L}, U={U}")
            print(f"  Expected: {result2}, Got: {result1}")
            failed_cases.append((a, b, L, U, result2, result1))
            all_passed = False
        else:
            print(f"PASS: a={a}, b={b}, L={L}, U={U} -> {result1}")
    except Exception as e:
        print(f"ERROR: a={a}, b={b}, L={L}, U={U} - {e}")
        failed_cases.append((a, b, L, U, "ERROR", str(e)))
        all_passed = False

if all_passed:
    print("\n[SUCCESS] All edge cases passed!")
else:
    print(f"\n[FAILED] {len(failed_cases)} test case(s) failed!")
    print("\nFailed cases:")
    for a, b, L, U, expected, got in failed_cases:
        print(f"  a={a}, b={b}, L={L}, U={U}: Expected {expected}, Got {got}")
