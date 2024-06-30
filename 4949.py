while(1):
    small = 0
    big = 0
    world = input()

    if world == '.':
        break

    for t in world:
        if t == '(':
            small += 1
        elif t == ')':
            small -= 1
        elif t == '[':
            big += 1
        elif t == ']':
            big -= 1
        if small < 0 or big < 0:
            print('no')
            break
    if small == 0 and big == 0:
        print('yes')
