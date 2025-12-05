import sys
input = sys.stdin.readline

cnt = int(input())

measures = list(map(int,input().split()))
if cnt == 1:
    print(measures[0] ** 2)
else:
    print(max(measures) * min(measures))