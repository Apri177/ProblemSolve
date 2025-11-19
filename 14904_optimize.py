import queue
import sys
input = sys.stdin.readline

inf = 1e9+7

class Node:
    def __init(self, data):
        self.head = None
        self.tail = None
    
    def push(self, node):
        if self.head == None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = self.tail.next
        
        def pop(self):
            if self.head == None:
                return -1
            
            v = self.head.data
            self.head = self.head.next
            
            if self.head == None:
                self.tail = None
            
            return v
        
        def is_empty(self):
            return self.head == None
        
class edge:
    def __init__(self, v, dual, cap, dst):
        self.v = v
        self.dual = dual
        self.cap = cap
        self.dst = dst
    
n, k = map(int, input().split())

board = []
for i in range(n):
    board.extend([*map(int, input().split())])

#진짜 -> 진짜는 1
#가짜 -> 진짜는 k-1
#현재진짜 -> 가짜는 k-1

D = n**2
S = 0
E = 2 * D - 1

adj = [[] for _ in range(E + 1)]

def add(s, e, cap, dst):
    adj[s].append(edge(e, len(adj[e]), cap, dst))
    adj[e].append(edge(s,len(adj[s]) - 1, 0, -dst))

for i in range(n):
    for j in range(n):
        now = i * n + j
        add(now, now+D, 1, -board[now])
        add(now, now + D, k - 1, 0)
        if i + 1 < n: add(now + D, now + n, k , 0)
        if j + 1 < n: add(now + D, now + 1, k , 0)

ans = 0

while 1:
    q = queue()
    inq = [0] * (E + 1)
    dst = [inf] * (E + 1)
    par = [-1] * (E + 1)
    idx = [-1] * (E + 1)
    q.push(Node(S))
    inq[S] = 1
    dst[S] = 0
    while(not q.is_empty()):
        now = q.pop()
        inq[now] = 0
        for x in range(len(adj[now])):
            i = adj[now][x]
            nxt = i.v
            cap = i.cap
            ndst = i.dst
            if cap > 0 and dst[now] + ndst < dst[nxt]:
                dst[nxt] = dst[now] + ndst
                par[nxt] = now;
                idx[nxt] = x
                if not inq[nxt]:
                    inq[nxt] = 1
                    q.push(Node(nxt))
    if par[E] == -1: break
    flow = inf
    now = E
    while now!=S:
        a = par[now]
        b = idx[now]
        flow = min(flow, adj[a][b].cap)
        now = par[now]
    now = E
    while now!=S:
        a = par[now]
        b = idx[now]
        ans += flow * adj[a][b].dst
        adj[now][adj[a][b].dual].cap += flow
        now = par[now]
print(-ans)