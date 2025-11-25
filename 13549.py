from collections import deque
import sys
input = sys.stdin.readline

N, K = map(int, input().split())

inf = float('inf')
dist = [inf] * 100001

dist[N] = 0
d = deque()
d.append(N)

while d:
    vertex = d.popleft()
    
    if vertex == K:
        break
    
    if vertex * 2 <= 100000 and dist[vertex * 2] > dist[vertex]:
        dist[vertex * 2] = dist[vertex]
        d.appendleft(vertex * 2)
    if vertex + 1 <= 100000 and dist[vertex + 1] > dist[vertex] + 1:
        dist[vertex + 1] = dist[vertex] + 1
        d.append(vertex + 1)
    if vertex - 1 >= 0 and dist[vertex - 1] > dist[vertex] + 1:
        dist[vertex - 1] = dist[vertex] + 1
        d.append(vertex - 1)
    
print(dist[K])