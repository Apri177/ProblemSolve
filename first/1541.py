formula = input().split('-')

num = []

for i in formula:
    sum = 0
    temp = i.split('+')
    for j in temp:
        sum += int(j)
    num.append(sum)

ans = num[0]
for i in range(1, len(num)):
    ans -= num[j]
print(ans)