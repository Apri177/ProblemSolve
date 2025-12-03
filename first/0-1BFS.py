from collections import deque
import sys

def zero_one_bfs(graph, start, n):
    """
    0-1 BFS 알고리즘
    graph: 인접 리스트 형태의 그래프 [(인접 정점, 가중치), ...]
    start: 시작 정점
    n: 정점의 개수
    """
    INF = float('inf')
    dist = [INF] * n
    
    dist[start] = 0
    d = deque()
    d.append(start)
    
    while d:
        vertex = d.popleft()
        
        for u, weight in graph[vertex]:
            # 간선을 통해 거리가 완화되는지 확인
            if dist[u] > dist[vertex] + weight:
                dist[u] = dist[vertex] + weight
                
                if weight == 1:
                    d.append(u)  # 가중치가 1이면 뒤에 추가
                else:
                    d.appendleft(u)  # 가중치가 0이면 앞에 추가
    
    return dist

# 사용 예시
if __name__ == "__main__":
    # 예시 그래프 (정점 5개)
    n = 5
    graph = [[] for _ in range(n)]
    
    # 간선 추가 (정점, 가중치)
    graph[0].append((1, 0))  # 0 -> 1 (가중치 0)
    graph[0].append((2, 1))  # 0 -> 2 (가중치 1)
    graph[1].append((2, 0))  # 1 -> 2 (가중치 0)
    graph[1].append((3, 1))  # 1 -> 3 (가중치 1)
    graph[2].append((4, 1))  # 2 -> 4 (가중치 1)
    graph[3].append((4, 0))  # 3 -> 4 (가중치 0)
    
    dist = zero_one_bfs(graph, 0, n)
    print("시작 정점 0에서의 최단 거리:")
    for i in range(n):
        print(f"정점 {i}: {dist[i]}")

