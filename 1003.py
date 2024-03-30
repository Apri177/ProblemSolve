z = [1, 0, 1]
o = [0, 1, 1]

def ans(n):
    l = len(z)
    if n >= l:
        for i in range(l, n + 1):
            z.append(z[i - 1] + z[i - 2])
            o.append(o[i - 1] + o[i - 2])
    print(z[n], o[n])

for _ in range(int(input())):
    ans(int(input()))