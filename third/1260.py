from collections import deque
import sys
input = sys.stdin.readline

N, M, V = map(int,input().split())
temp = V
arr = [[] for _ in range(N + 1)]
for _ in range(M):
    a, b = map(int,input().split())
    arr[a].append(b)
    arr[b].append(a)

queue = []
queue.append(V)
for _ in range(M):
    for i in sorted(arr[V]):
        if queue.count(i) == 0:
            queue.append(i)
            V = i
            break
print(*queue)

V = temp
queue = []
stack = deque()
stack.append(V)
for _ in range(M + 1):
    for i in sorted(stack):
        if queue.count(i) == 0:
            queue.append(i)
            for j in arr[stack.popleft()]:
                stack.append(j)
print(*queue)

            
        
            

            
            