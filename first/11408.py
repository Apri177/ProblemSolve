import sys
input = sys.stdin.readline

# 첫 줄: 직원 수 N, 일의 개수 M
N, M = map(int, input().split())

# 각 직원이 할 수 있는 일의 정보
# 각 줄: k (할 수 있는 일의 개수) + k개의 일 번호
employees = []
for _ in range(N):
    data = list(map(int, input().split()))
    k = data[0]
    jobs = data[1:1+k]  # 일 번호들 (1-indexed)
    employees.append(jobs)
