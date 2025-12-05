import sys
input = sys.stdin.readline

N = int(input())
count = 0
for i in range(1, N + 1):
    count += i * (N // i)
print(count)
    