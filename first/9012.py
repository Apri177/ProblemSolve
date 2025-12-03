for _ in range(int(input())):
    w = 0
    for n in input():
        if w < 0:
            break

        if n == '(':
            w += 1
        else:
            w -= 1
        
    if w == 0:
        print('YES')
    else:
        print('NO')
