import sys
input = sys.stdin.readline

t = int(input().strip())
targets = [int(input().strip()) for _ in range(t)]
max_n = max(targets) if targets else 0

dp = [(0, 0)] * (max_n + 1 if max_n >= 1 else 2)
dp[0] = (1, 0)
dp[1] = (0, 1)

for i in range(2, max_n + 1):
    dp[i] = (dp[i - 1][0] + dp[i - 2][0], dp[i - 1][1] + dp[i - 2][1])

for n in targets:
    print(dp[n][0], dp[n][1])