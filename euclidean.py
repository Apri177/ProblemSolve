def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b / gcd(a, b)


def EEA(r1, r2, u1, u2, v1, v2):
    if r2 == 0:
        print(f'gcd : {r1}, u: {u1}, v: {v1}')
        return 
    q  = r1 // r2
    r = r1 % r2
    u = u1 - q * u2
    v = v1 - q * v2

    return EEA(r2, r, u2, u, v2, v)
