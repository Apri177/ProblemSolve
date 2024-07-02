import sys
from collections import deque
input = sys.stdin.readline

n = int(input())
tree = [[] for _ in range(n + 1)] # Connected graph

for _ in range(n):
    diameter = list(map(int, input().split()))
    cnt_node = diameter[0]
    idx = 1
    while diameter[idx] != -1:
        adj_node, adj_cost = diameter[idx], diameter[idx + 1]
        tree[cnt_node].append((adj_node, adj_cost))
        idx += 2

visited = [-1] * (n + 1)
visited[1] = 0

# none return, save distance of each nodes in visited
def dfs(node, dist):
    for v, d in tree[node]:
        cal_dist = dist + d
        if visited[v] ==  -1:
            visited[v] = cal_dist
            dfs(v, cal_dist)
    return

dfs(1, 0)
tmp = [0, 0]

# find most high distance node
for i in range(1, len(visited)):
    if visited[i] > tmp[1]:
        tmp[1] = visited[i]
        tmp[0] = i

visited = [-1] * (n + 1)
visited[tmp[0]] = 0
dfs(tmp[0], 0)

print(max(visited))