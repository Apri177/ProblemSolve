
import sys
import math
input = sys.stdin.readline
cnt = 0
n = int(input())
for i in str(math.factorial(n))[::-1]:
    if i!= '0':
        break
    cnt += 1
print(cnt)