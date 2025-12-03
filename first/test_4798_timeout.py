import sys
import math
import time
import importlib.util
from contextlib import contextmanager

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

is_prime_sieve = module_4798.is_prime_sieve
primes = module_4798.primes
count_primes = module_4798.count_primes

@contextmanager
def timeout(seconds):
    import signal
    
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Timeout after {seconds} seconds")
    
    if sys.platform != 'win32':
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
    else:
        start_time = time.time()
        yield
        elapsed = time.time() - start_time
        if elapsed > seconds:
            raise TimeoutError(f"Timeout after {seconds} seconds")

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
    (1, 2, 0, 10000),
    (2, 1, 0, 10000),
    (1, 0, 0, 10000),
    (1, 1, 0, 10000),
    (100, 97, 0, 1000),
    (1000, 997, 0, 1000),
    (1, 2, 0, 100000),
    (2, 1, 0, 100000),
    (1, 0, 0, 100000),
    (1, 2, 0, 500000),
    (2, 1, 0, 500000),
    (1, 0, 0, 500000),
    (1, 2, 0, 1000000),
    (2, 1, 0, 1000000),
    (1, 0, 0, 1000000),
    (1000000, 999983, 0, 1000),
    (100000, 99997, 0, 10000),
    (10000, 9973, 0, 100000),
]

print("Testing with 1 second timeout per test case...")
print("=" * 60)

all_passed = True
timeout_cases = []
failed_cases = []
total_time = 0
test_count = 0

for a, b, L, U in test_cases:
    if a * U + b > 10**12:
        continue
    if U - L > 10**6:
        continue
    
    test_count += 1
    start_time = time.time()
    
    try:
        result1 = None
        result2 = None
        
        elapsed = time.time() - start_time
        if elapsed > 1.0:
            print(f"TIMEOUT: a={a}, b={b}, L={L}, U={U} (before execution)")
            timeout_cases.append((a, b, L, U))
            all_passed = False
            continue
        
        start_time = time.time()
        result1 = count_primes(a, b, L, U, is_prime_sieve, primes)
        elapsed1 = time.time() - start_time
        
        if elapsed1 > 1.0:
            print(f"TIMEOUT: a={a}, b={b}, L={L}, U={U} ({elapsed1:.3f}s)")
            timeout_cases.append((a, b, L, U))
            all_passed = False
            continue
        
        start_time = time.time()
        result2 = count_primes_naive(a, b, L, U)
        elapsed2 = time.time() - start_time
        
        total_time += elapsed1
        
        if result1 != result2:
            print(f"FAIL: a={a}, b={b}, L={L}, U={U} ({elapsed1:.3f}s)")
            print(f"  Expected: {result2}, Got: {result1}")
            failed_cases.append((a, b, L, U, result2, result1, elapsed1))
            all_passed = False
        else:
            status = "OK" if elapsed1 < 0.1 else "SLOW" if elapsed1 < 0.5 else "WARN"
            print(f"PASS: a={a}, b={b}, L={L}, U={U} -> {result1} ({elapsed1:.3f}s) [{status}]")
            
    except TimeoutError as e:
        elapsed = time.time() - start_time
        print(f"TIMEOUT: a={a}, b={b}, L={L}, U={U} ({elapsed:.3f}s)")
        timeout_cases.append((a, b, L, U))
        all_passed = False
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"ERROR: a={a}, b={b}, L={L}, U={U} ({elapsed:.3f}s) - {e}")
        failed_cases.append((a, b, L, U, "ERROR", str(e), elapsed))
        all_passed = False

print("=" * 60)
print(f"\nTest Summary:")
print(f"  Total test cases: {test_count}")
print(f"  Passed: {test_count - len(failed_cases) - len(timeout_cases)}")
print(f"  Failed: {len(failed_cases)}")
print(f"  Timeout: {len(timeout_cases)}")
print(f"  Total execution time: {total_time:.3f}s")
print(f"  Average time per test: {total_time / max(1, test_count - len(timeout_cases)):.3f}s")

if timeout_cases:
    print(f"\nTimeout cases ({len(timeout_cases)}):")
    for a, b, L, U in timeout_cases[:10]:
        print(f"  a={a}, b={b}, L={L}, U={U}")
    if len(timeout_cases) > 10:
        print(f"  ... and {len(timeout_cases) - 10} more")

if failed_cases:
    print(f"\nFailed cases ({len(failed_cases)}):")
    for a, b, L, U, expected, got, elapsed in failed_cases[:10]:
        print(f"  a={a}, b={b}, L={L}, U={U}: Expected {expected}, Got {got} ({elapsed:.3f}s)")
    if len(failed_cases) > 10:
        print(f"  ... and {len(failed_cases) - 10} more")

if all_passed and not timeout_cases:
    print("\n[SUCCESS] All test cases passed within 1 second!")
elif timeout_cases:
    print(f"\n[WARNING] {len(timeout_cases)} test case(s) exceeded 1 second timeout!")
else:
    print("\n[FAILED] Some test cases failed!")

