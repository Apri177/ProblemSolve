import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6)


T = int(input())
for _ in range(T):
    M, N, K = map(int, input().split())
    arr = [[0] * M for _ in range(N)]
    for _ in range(K):
        x, y = map(int,input().split())
        arr[y][x] = 1
    
    def dfs(y, x):
        arr[y][x] = 0
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]
        
        for i in range(4):
            ax = x + dx[i]
            ay = y + dy[i]
            
            if 0 <= ay < N and 0 <= ax < M and arr[ay][ax] == 1:
                dfs(ay, ax)
    
    ans = 0
    for y in range(N):
        for x in range(M):
            if arr[y][x] == 1:
                dfs(y, x)
                ans += 1
                
    print(ans)