import sys
sys.setrecursionlimit(10 ** 8)

N, r, c = map(int, input().split())

answer = 0

while N > 0:
    N -= 1
    half = 1 << N
    block_size = half * half
    if r < half and c < half:
        # 1사분면(왼쪽 위)
        pass
    elif r < half and c >= half:
        # 2사분면(오른쪽 위)
        answer += block_size
        c -= half
    elif r >= half and c < half:
        # 3사분면(왼쪽 아래)
        answer += 2 * block_size
        r -= half
    else:
        # 4사분면(오른쪽 아래)
        answer += 3 * block_size
        r -= half
        c -= half

print(answer)
