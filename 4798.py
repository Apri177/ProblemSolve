import sys
import math

def sieve_of_eratosthenes(max_num):
    is_prime = [True] * (max_num + 1)
    p = 2
    while (p * p <= max_num):
        if is_prime[p] == True:
            for i in range(p * p, max_num + 1, p):
                is_prime[i] = False
        p += 1
    prime_numbers = []
    for p in range(2, max_num + 1):
        if is_prime[p]:
            prime_numbers.append(p)
    return prime_numbers, is_prime

def is_prime(n, prime_list):
    if n <= len(prime_list) - 1:
        return prime_list[n]
    if n < 2:
        return False
    for prime in prime_numbers:
        if prime * prime > n:
            break
        if n % prime == 0:
            return False
    return True

test_case_num = 0
# input = sys.stdin.readlines().strip().split('\n')

max_possible_value = 10**6
prime_numbers, is_prime_list = sieve_of_eratosthenes(max_possible_value)


while True:
    try: 
        line = input()
        
        if line == "0":
            break

        a, b, L, U = map(int, line.split())

        test_case_num += 1
        count = 0
        for n in range(L, U + 1):
            t_n = a * n + b
            if is_prime(t_n, is_prime_list):
                count += 1
        print(f"Case {test_case_num}: {count}")
    except:
        break


# for line in input:

#     if line == "0":
#         break

#     a, b, L, U = map(int, line.split())

#     test_case_num += 1
#     count = 0
#     for n in range(L, U + 1):
#         t_n = a * n + b
#         if is_prime(t_n, is_prime_list):
#             count += 1
#     print(f"Case {test_case_num}: {count}")