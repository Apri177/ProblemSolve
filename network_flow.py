import sys
from collections import deque
input = sys.stdin.readline
iunput = sys.stdin.readline
MAX = 1e9

def fordFulkerson(graph, s, t, n):
    # graph는 그래프 및 간선의 비용 정보
    # s는 시작노드
    # t는 목적지 노드
    # n은 노드의 개수 
    remain = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            remain[i][j] = graph[i][j]
    max_flow = 0 # 최대 유량
    while True: # bfs
        visited = [False] * n
        queue = deque()
        queue.append(s)
        visited[s] = True
        path = [-1] * n # 경로, 부모 노드를 저장. 거슬러 올라가면 경로를 구할 수 있음
        path[s] = -1 # 처음 노드는 부모 노드가 없음
        
        while queue:
            a = queue.popleft()
            for b in range(n):
                if not visited[b] and remain[a][b] > 0: # 방문하지 않았고 갈 수 있다면
                    queue.append(b)
                    path[b] = a
                    visited[b] = True
        if not visited[t]: # 목적지로 가는 경로가 없다면
            break
    # 경로는 도착 노드인 t 부터 path를 보면서 부모 노드를 거슬러 올라가면 됨
    # path[b] = a의 의미는 s에서 t로 도달하는 경로 중 a 노드에서 b노드로 가는 경로가 있다는 뜻이다.
    # path에는 부모 노드를 계속 저장하는데 이는 곧 경로를 의미한다.
    # 만약 s -> a -> b -> t 라는 경로가 있다면
    # path[s] = a, path[a] = b, path[t] = b가 저장되어 있을 것이다.
    # 이러면 t부터 거꾸로 거슬러 올라가면 t -> b -> a -> s 경로를 알 수 있고 이를 뒤집은 경로가 bfs가 찾은 경로이다.
    # 물론 연결만 되어있다면 모든 노드를 방문하기 때문에 c와 d에도 부모 노드가 저장되어 있겠지만 t부터 거슬러 올라가면 c와 d는 경로에 추가되지 않는다.
    # 이제 하나의 경로를 구했으니 유량을 흘려보낼 차례이다.
    # 당연히 이 경로로 흘려 보낼 수 있는 유량의 최대 크기는 간선들의 남아있는 용량 중 가장 작은 값이다
    # 다음과 같은 간선들의 남아있는 용량이 있다고 하면 가장 작은 값인 3보다 크게 보낼 수는 없을 것이다.
    # 이제 경로를 통해 간선들의 남아있는 용량 중 가장 작은 값을 알아내야 한다.
    
    b = t # 경로를 거슬러 올라가기 위한 변수
    min_remain = MAX # 경로 간선들 중 가장 작은 용량을 구하기 위한 변수
    while b != s: # 처음 노드에 도착할 때까지
        a = path[b]
        min_remain = min(min_remain, remain[a][b])
        b = a
    
    # 경로를 거슬러 올라가면서 가장 작은 남아있는 용량을 알아낸다. 이제 이 용량만큼 유량을 흘려보내면 된다.
    
    while b != s:
        a = path[b]
        remain[a][b] -= min_remain
        remain[b][a] += min_remain
        b = a
    max_flow += min_remain
    return max_flow
    
    # 여기서 remain[a][b] -= min_remain을 통해 흘려보낸 유량만큼 남아있는 용량을 뺐다.
    # 그런데 remain[b][a] += min_remain은 무엇을 의미할까?
    # 포드 풀커슨 알고리즘에서 유량의 대칭성이 작용한다.
    # a -> b로 k만큼 유량을 흘려 보냈다면 b -> a로 유량을 흘려보낼 때 -k만큼 유량을 흘려보내면 같다라는 성질이다.
    
    # 이 성질에 의해서 원래 없었던 경로를 만들어 주는 것이다.
    # 새로운 경로가 만들어졌으므로 다시 한 번 bfs를 실시한다.
    # 이번에는 새로 만들어진 경로를 통해 s -> a -> c -> d -> t에 해당하는 경로를 찾았다고 가정한다.
    # 똑같은 과정을 반복하면 또 새로운 경로가 생긴다.
    
    # 이렇게 반복을 하다보면 bfs를 끝냈음에도 t에 방문하지 않은 경우가 생길 것이다.
    # 이것이 곧 더 이상 유량을 보낼 수 없는 상황에 도달했다는 것이고 그 때 반복을 종료하면 된다.
    