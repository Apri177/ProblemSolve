arr = []
ex = [0, 0, 1, -1]
ey = [1, -1, 0, 0]

def dfs(x, y):
    for i in range(4):
        x += ex[i]
        y += ey[i]
        if(0 <= x < m) and (0 <= y < n):
            if arr[y][x] == 1:
                arr[y][x] = 0
                dfs(x, y)
        
for _ in range(int(input())):
    m, n, k = map(int,input().split())
    arr = [[0 for _ in range(m)] for _ in range(n)]
    cnt = 0
    for _ in range(k):
        x, y = map(int,input().split())
        arr[y][x] = 1
    for x in range(m):
        for y in range(n):
            if arr[y][x] == 1:
                dfs(x, y)
                cnt += 1
    print(cnt)

