import sys
input = sys.stdin.readline

N, B = map(int, input().split())
A = []
for _ in range(N):
    A.append(list(map(int, input().split())))

MOD = 1000 

def square_matrix(A_matrix : list, B_matrix : list) -> list:
    c = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                c[i][j] = (c[i][j] + A_matrix[i][k] * B_matrix[k][j]) % MOD
    
    return c
                
def power(matrix, power):
    result = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    
    base = matrix
    
    while power > 0:
        if power % 2 == 1:
            result = square_matrix(result, base)
        base = square_matrix(base, base)
        power //= 2
    return result
        
result = power(A, B)
for i in result:
    print(' '.join(map(str, i)))
    