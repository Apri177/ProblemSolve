import sys
from collections import Counter

input = sys.stdin.readline

n = int(input())

numbers = []
for _ in range(n):
    numbers.append(int(input()))

numbers.sort()

mean = round(sum(numbers) / n)

median = numbers[n // 2]

counter = Counter(numbers)
max_count = max(counter.values())
modes = [num for num, count in counter.items() if count == max_count]
modes.sort()
mode = modes[0] if len(modes) == 1 else modes[1]

range_value = numbers[-1] - numbers[0]

print(mean)
print(median)
print(mode)
print(range_value)