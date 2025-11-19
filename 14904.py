import sys
from collections import deque

class Edge:
    def __init__(self, to, capacity, cost, rev):
        self.to = to
        self.capacity = capacity
        self.cost = cost
        self.rev = rev

class MCMF:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.dist = [0] * n
        self.prevv = [0] * n
        self.preve = [0] * n
    
    def add_edge(self, fr, to, capacity, cost):
        self.graph[fr].append(Edge(to, capacity, cost, len(self.graph[to])))
        self.graph[to].append(Edge(fr, 0, -cost, len(self.graph[fr]) - 1))
    
    def min_cost_flow(self, s, t, f):
        res = 0
        flow = 0
        while flow < f:
            INF = 10**18
            self.dist = [INF] * self.n
            self.dist[s] = 0
            inq = [False] * self.n
            q = deque([s])
            inq[s] = True
            
            while q:
                v = q.popleft()
                inq[v] = False
                for i, edge in enumerate(self.graph[v]):
                    if edge.capacity > 0 and self.dist[edge.to] > self.dist[v] + edge.cost:
                        self.dist[edge.to] = self.dist[v] + edge.cost
                        self.prevv[edge.to] = v
                        self.preve[edge.to] = i
                        if not inq[edge.to]:
                            q.append(edge.to)
                            inq[edge.to] = True
            
            if self.dist[t] == INF:
                return -1
            
            d = f - flow
            v = t
            while v != s:
                edge = self.graph[self.prevv[v]][self.preve[v]]
                d = min(d, edge.capacity)
                v = self.prevv[v]
            
            flow += d
            res += d * self.dist[t]
            
            v = t
            while v != s:
                edge = self.graph[self.prevv[v]][self.preve[v]]
                edge.capacity -= d
                self.graph[edge.to][edge.rev].capacity += d
                v = self.prevv[v]
        
        return res

def solve():
    N, K = map(int, input().split())
    maze = [list(map(int, input().split())) for _ in range(N)]
    
    total_nodes = 2 * N * N
    mcmf = MCMF(total_nodes)
    
    for r in range(N):
        for c in range(N):
            in_node = r * N + c
            out_node = N * N + r * N + c
            
            mcmf.add_edge(in_node, out_node, 1, -maze[r][c])
            
            if K > 1:
                mcmf.add_edge(in_node, out_node, K - 1, 0)
    
    for r in range(N):
        for c in range(N - 1):
            out_node = N * N + r * N + c
            next_in_node = r * N + (c + 1)
            mcmf.add_edge(out_node, next_in_node, K, 0)
    
    for r in range(N - 1):
        for c in range(N):
            out_node = N * N + r * N + c
            next_in_node = (r + 1) * N + c
            mcmf.add_edge(out_node, next_in_node, K, 0)
    
    start = 0
    end = N * N + (N - 1) * N + (N - 1)
    
    result = mcmf.min_cost_flow(start, end, K)
    
    if result == -1:
        print(-1)
    else:
        print(-result)

if __name__ == '__main__':
    solve()