
def find(x):
    if parent[x] != x:
        return find(parent[x])
    return x

# 특정 원소가 속한 집합 찾기
def find_parent(x):
    # 루트 노드가 아니라면 루트노드를 찾을 때까지 재귀적으로 탐색
    if parent[x] != x:
        parent[x] = find_parent(parent[x])
    return parent[x]

# 큰 집합에 작은 집합 합치기
def union(a, b):
    a = find(a)
    b = find(b)
    if a < b:
        parent[b] = a
    else:
        parent[a] = b


n, m = map(int, input().split()) # 노드의 개수와 간선의 개수(union 연산의 수) 입력
parent = [0] * (n + 1) # 부모 테이블 초기화

for i in range(1, n + 1):
    parent[i] = i

# Union 연산 수행 부분
for i in range(m):
    a, b = map(int, input().split())
    union(a, b)

print('각 원소가 속한 집합: ', end = " ")
for i in range(1, n + 1):
    print(find(i))

print('부모 테이블: ')
for i in range(1, n + 1):
    print(parent[i])
    
