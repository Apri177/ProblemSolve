# from collections import deque

# def bfs(graph, start, visited):
#     queue = deque([start])
#     visited[start] = True

#     while queue:
#         v = queue.popleft()

#         for i in graph[v]:
#             if not visited[i]:
#                 queue.append(i)
#                 visited[i] = True

# n, m = map(int, input().split())
# graph = [[] for _ in range(n + 1)]

# for i in range(m):
#     u, v = map(int, input().split())
#     graph[u].append(v)
#     graph[v].append(u)

# cnt = 0
# visited = [False] * (n + 1)
# for i in range(1, n + 1):
#     if not visited[i]:
#         bfs(graph, i, visited)
#         cnt += 1

# print(cnt)


from collections import deque  # deque를 사용하여 BFS 구현

def bfs(graph, start, visited):
    queue = deque([start])  # 시작 노드를 큐에 추가
    visited[start] = True  # 시작 노드를 방문 처리

    while queue:  # 큐가 빌 때까지 반복
        v = queue.popleft()  # 큐의 앞에서 노드를 하나 꺼냄

        for i in graph[v]:  # 현재 노드의 인접 노드를 순회
            if not visited[i]:  # 인접 노드를 방문하지 않았다면
                queue.append(i)  # 큐에 인접 노드를 추가
                visited[i] = True  # 인접 노드를 방문 처리

n, m = map(int, input().split())  # 노드의 수(n)와 간선의 수(m)를 입력받음
graph = [[] for _ in range(n + 1)]  # 노드 번호를 1부터 사용하기 위해 (n+1) 크기의 인접 리스트 생성

for i in range(m):  # m개의 간선을 입력받음
    u, v = map(int, input().split())  # 간선의 양 끝 노드 u와 v를 입력받음
    graph[u].append(v)  # 노드 u에 노드 v를 추가 (양방향 그래프)
    graph[v].append(u)  # 노드 v에 노드 u를 추가 (양방향 그래프)

cnt = 0  # 연결 요소의 수를 세기 위한 변수
visited = [False] * (n + 1)  # 노드 방문 여부를 기록하는 리스트, 처음엔 모두 방문하지 않은 상태로 초기화
for i in range(1, n + 1):  # 1번 노드부터 n번 노드까지 순회
    if not visited[i]:  # 현재 노드를 방문하지 않았다면
        bfs(graph, i, visited)  # 현재 노드를 시작으로 BFS 실행
        cnt += 1  # 연결 요소의 수 증가

print(cnt)  # 연결 요소의 수를 출력