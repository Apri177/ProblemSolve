import sys
input = sys.stdin.readline

N = int(input())
piles = list(map(int, input().split()))

nim_sum = 0
for pile in piles:
    nim_sum ^= pile
    
if nim_sum == 0:
    print(0)
else:
    count = 0
    for pile in piles:
        if pile > (nim_sum ^ pile):
            count += 1
    
    print(count)