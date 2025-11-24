#백조의 호수 (0-1 BFS 최적화)
from collections import deque
import sys
input = sys.stdin.readline

r, c = map(int, input().split())
arr = [list(input().strip()) for _ in range(r)]
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

# 백조 위치 찾기
swans = []
for i in range(r):
    for j in range(c):
        if arr[i][j] == 'L':
            swans.append((i, j))

# 0-1 BFS: 한 백조에서 다른 백조까지의 최단 일수 구하기
INF = float('inf')
dist = [[INF] * c for _ in range(r)]
start_x, start_y = swans[0]
end_x, end_y = swans[1]

dist[start_x][start_y] = 0
d = deque()
d.append((start_x, start_y))

while d:
    x, y = d.popleft()
    
    # 다른 백조에 도달했으면 종료
    if (x, y) == (end_x, end_y):
        for i in range(r):
            for j in range(c):
                print(dist[i][j], end=" ")
            print()
        # print(dist[x][y])
        break
        print()
    
    for i in range(4):
        nx, ny = x + dx[i], y + dy[i]
        if 0 <= nx < r and 0 <= ny < c:
            # 거리 완화 확인
            if arr[nx][ny] == 'X':
                # 얼음: 가중치 1 (하루 기다려야 녹음)
                weight = 1
            else:
                # 물('.') 또는 백조('L'): 가중치 0 (즉시 이동 가능)
                weight = 0
            
            if dist[nx][ny] > dist[x][y] + weight:
                dist[nx][ny] = dist[x][y] + weight
                
                if weight == 1:
                    d.append((nx, ny))  # 가중치 1이면 뒤에 추가
                else:
                    d.appendleft((nx, ny))  # 가중치 0이면 앞에 추가