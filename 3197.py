#백조의 호수
from collections import deque
import sys
input = sys.stdin.readline

r, c = map(int, input().split())
arr = [list(input().strip()) for _ in range(r)]
visited = [[False] * c for _ in range(r)]
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

cnt = 0

def bfs(x, y):
    q = deque()
    q.append((x, y))
    visited[x][y] = True
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 <= nx < r and 0 <= ny < c and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))

for i in range(r):
    for j in range(c):
        if arr[i][j] == 'X':
            bfs(i, j)

print(cnt)