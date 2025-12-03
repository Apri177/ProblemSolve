import sys
input = sys.stdin.readline

n, m = map(int, input().split()) # 사람 수, 파티 수 입력
peopleList = set(input().split()[1:]) # 거짓말을 아는 사람 수, 번호 입력
party = [] # 파티의 정보를 받을 리스트 생성

for _ in range(m):
    party.append(set(input().split()[1:])) # 파티의 정보

for _ in range(m):
    for p in party:
        if p & peopleList: # 파티에 거짓말을 아는 사람이 있으면
            peopleList = peopleList.union(p) # 거짓말을 아는 사람의 튜플에 파티의 인원 유니온

cnt = 0
for p in party:
    if p & peopleList:
        continue
    cnt += 1

print(cnt)