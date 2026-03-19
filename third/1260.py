# from collections import deque
# import sys
# input = sys.stdin.readline

# N, M, V = map(int,input().split())
# temp = V
# arr = [[] for _ in range(N + 1)]
# for _ in range(M):
#     a, b = map(int,input().split())
#     arr[a].append(b)
#     arr[b].append(a)

# queue = []
# queue.append(V)
# for _ in range(M):
#     for i in sorted(arr[V]):
#         if queue.count(i) == 0:
#             queue.append(i)
#             V = i
#             break
# print(*queue)

# V = temp
# queue = []
# stack = deque()
# stack.append(V)
# for _ in range(M + 1):
#     for i in sorted(stack):
#         if queue.count(i) == 0:
#             queue.append(i)
#             for j in arr[stack.popleft()]:
#                 stack.append(j)
# print(*queue)


import sys
from collections import deque
input = sys.stdin.readline
sys.setrecursionlimit(10000)

N, M, V = map(int, input().split())
adj = [[] for _ in range(N + 1)]

for _ in range(M):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

# 한 번만 정렬
for i in range(N + 1):
    adj[i].sort()

# DFS (재귀)
visited = [False] * (N + 1)
dfs_result = []

def dfs(v):
    visited[v] = True
    dfs_result.append(v)
    for nv in adj[v]:
        if not visited[nv]:
            dfs(nv)

dfs(V)
print(*dfs_result)

# BFS
visited = [False] * (N + 1)
bfs_result = []
queue = deque([V])
visited[V] = True

while queue:
    v = queue.popleft()
    bfs_result.append(v)
    for nv in adj[v]:
        if not visited[nv]:
            visited[nv] = True
            queue.append(nv)

print(*bfs_result)

