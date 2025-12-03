import sys
input = sys.stdin.readline

n = int(input())
house = []
dp = [[0] * 3 for _ in range(n)]

for i in range(n):
    house.append(list(map(int,input().split())))
dp[0][0] = house[0][0]
dp[0][1] = house[0][1]
dp[0][2] = house[0][2]
for i in range(1, n):
    dp[i][0] = min(house[i][0] + dp[i - 1][1], house[i][0] + dp[i - 1][2])
    dp[i][1] = min(house[i][1] + dp[i - 1][0], house[i][1] + dp[i - 1][2])
    dp[i][2] = min(house[i][2] + dp[i - 1][0], house[i][2] + dp[i - 1][1])
print(min(dp[-1]))