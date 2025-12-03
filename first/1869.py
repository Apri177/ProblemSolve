import sys
input = sys.stdin.readline

def get(seq):
    n = len(seq)
    candidates = []
    
    curr = list(seq)
    
    for _ in range(n):
        candidates.append(tuple(curr))
        curr = curr[1:] + curr[:1]
    
    curr = list(seq)[::-1]
    for _ in range(n):
        candidates.append(tuple(curr))
        curr = curr[1:] + curr[:1]
    
    return min(candidates)

N = int(input().strip())
sticks = list(map(int, input().split()))

stick_dist = {}
for i in sticks:
    stick_dist[i] = stick_dist.get(i, 0) + 1
kinds_sticks = sorted(stick_dist.keys())
        
diff_map = {}
for i in range(len(kinds_sticks)):
    for j in range(len(kinds_sticks)):
        u = kinds_sticks[i]
        v = kinds_sticks[j]
        diff = u - v
        
        if diff not in diff_map:
            diff_map[diff] = []
        diff_map[diff].append((u, v))
        
hexagons = set()
for diff, pairs in diff_map.items():
    for p1 in pairs:
        for p2 in pairs:
            for p3 in pairs:
                s1, s4 = p1
                s3, s6 = p2
                s5, s2 = p3
                
                current_hex = [s1, s2, s3, s4, s5, s6]
                
                temp_counts = {}
                possible = True
                
                for length in current_hex:
                    temp_counts[length] = temp_counts.get(length, 0) + 1
                    if temp_counts[length] > stick_dist.get(length, 0):
                        possible = False
                        break
                if possible:
                    hexagons.add(get(current_hex))
print(len(hexagons))