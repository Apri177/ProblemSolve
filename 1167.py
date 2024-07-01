import sys
from collections import deque

input = sys.stdin.readline

n = int(input())

tree = [[] for _ in range(n + 1)] # connected graph

def bfs(s):
    q = deque()
    q.append((s, 0))
    visitied = [-1] * (n + 1)
    visitied[s] = 0

    res = [0, 0]

    while q:
        cnt_node, cnt_dist = q.popleft()

        for adj_node, adj_dist in tree[cnt_node]:
            if visitied[adj_node] == -1:
                cal_dist = cnt_dist + adj_dist

                q.append((adj_node, cal_dist))
                visitied[adj_node] = cal_dist

                if res[1] < cal_dist:
                    res[0] = adj_node
                    res[1] = cal_dist
    return res

for _ in range(n):
    diameter = list(map(int, input().split()))

    cnt_node = diameter[0]

    idx = 1
    
    while diameter[idx] != -1:
        adj_node, adj_cost = diameter[idx], diameter[idx + 1]
        tree[cnt_node].append((adj_node, adj_cost))
        idx += 2

point, _ = bfs(1)
print(bfs(point)[1])
