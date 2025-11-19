import sys

input = sys.stdin.readline

# N 입력
n = int(input())

# N개의 정수 집합 입력
arr = set(map(int, input().split()))

# M 입력
m = int(input())

# M개의 정수 입력
search_numbers = list(map(int, input().split()))

# 각 수가 집합에 존재하는지 확인
for num in search_numbers:
    if num in arr:
        print(1)
    else:
        print(0)
