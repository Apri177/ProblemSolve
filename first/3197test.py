#백조의 호수
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

# 초기 물 위치에서 인접한 얼음들만 큐에 넣기 (다음 날 녹을 얼음들)
melt_q = deque()  # 다음 날 녹을 얼음들
visited_melt = [[False] * c for _ in range(r)]

for i in range(r):
    for j in range(c):
        if arr[i][j] == '.' or arr[i][j] == 'L':
            # 인접한 얼음만 찾아서 큐에 추가
            for k in range(4):
                ni, nj = i + dx[k], j + dy[k]
                if 0 <= ni < r and 0 <= nj < c and arr[ni][nj] == 'X' and not visited_melt[ni][nj]:
                    melt_q.append((ni, nj))
                    visited_melt[ni][nj] = True

# 백조가 만날 수 있는지 확인하는 BFS
def can_meet():
    visited = [[False] * c for _ in range(r)]
    q = deque()
    start_x, start_y = swans[0]
    q.append((start_x, start_y))
    visited[start_x][start_y] = True
    
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < r and 0 <= ny < c and not visited[nx][ny]:
                if arr[nx][ny] == 'L' and (nx, ny) == swans[1]:
                    return True
                if arr[nx][ny] != 'X':  # 물이나 백조 위치면 이동 가능
                    visited[nx][ny] = True
                    q.append((nx, ny))
    return False

# 매일 얼음 녹이기
days = 0
while True:
    # 백조가 만날 수 있는지 확인
    if can_meet():
        print(days)
        break
    
    # 오늘 녹을 얼음들의 개수만큼만 처리
    today_melt = len(melt_q)
    for _ in range(today_melt):
        x, y = melt_q.popleft()
        arr[x][y] = '.'  # 얼음을 물로 변경
        
        # 새로 물이 된 위치에서 인접한 얼음만 찾아서 다음 날 녹을 큐에 추가
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < r and 0 <= ny < c and arr[nx][ny] == 'X' and not visited_melt[nx][ny]:
                visited_melt[nx][ny] = True
                melt_q.append((nx, ny))
    
    days += 1