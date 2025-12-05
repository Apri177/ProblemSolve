import sys
input = sys.stdin.readline

while 1:
    try:
        n = int(input())
    except:
        break;

    r = 0
    
    # 
    for i in range(1, n + 1):
        r = (r * 10 + 1) % n
        if r == 0:
            print(i)
            break
