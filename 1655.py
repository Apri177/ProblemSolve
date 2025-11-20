# 가운데를 말해요
import sys
import heapq
input = sys.stdin.readline

n = int(input())
max_heap = []
min_heap = []

for i in range(n):
    num = int(input())
    if len(max_heap) == len(min_heap):
        heapq.heappush(max_heap, -num)
    else:
        heapq.heappush(min_heap, num)
    if min_heap and -max_heap[0] > min_heap[0]:
        heapq.heappush(max_heap, -heapq.heappop(min_heap))
        heapq.heappush(min_heap, -heapq.heappop(max_heap))
    print(-max_heap[0])
    if i == n - 1:
        break
