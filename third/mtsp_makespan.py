"""
다중 외판원(mTSP) — 목표: 각 영업사원의 총 이동거리 중 최댓값 최소화.

휴리스틱: K-means++ → (선택) 크기/부하 균형 → 클러스터별 NN + 2-opt
입력: 첫 줄 N K, 이후 N줄 x y (좌표)
출력: K줄 — c_k, p_{k,1}, ... (도시 번호 1-based)
"""

from __future__ import annotations

import math
import random
import sys


def dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def dist_sq(a: tuple[float, float], b: tuple[float, float]) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy


def tour_length(tour: list[int], coords: list[tuple[float, float]]) -> float:
    n = len(tour)
    if n == 0:
        return 0.0
    if n == 1:
        return 0.0
    s = 0.0
    for i in range(n):
        s += dist(coords[tour[i]], coords[tour[(i + 1) % n]])
    return s


def two_opt_cycle(tour: list[int], coords: list[tuple[float, float]], max_rounds: int = 80) -> list[int]:
    """닫힌 경로에 대한 2-opt."""
    n = len(tour)
    if n < 4:
        return tour
    path = tour[:]
    rnd = 0
    while rnd < max_rounds:
        best_gain = 0.0
        best_ij: tuple[int, int] | None = None
        for i in range(n):
            a, b = path[i], path[(i + 1) % n]
            dab = dist(coords[a], coords[b])
            for j in range(i + 2, n):
                jn = (j + 1) % n
                if jn == i:
                    continue
                c, d = path[j], path[jn]
                dcd = dist(coords[c], coords[d])
                before = dab + dcd
                after = dist(coords[a], coords[c]) + dist(coords[b], coords[d])
                gain = before - after
                if gain > best_gain + 1e-12:
                    best_gain = gain
                    best_ij = (i, j)
        if best_ij is None or best_gain < 1e-12:
            break
        i, j = best_ij
        path[i + 1 : j + 1] = reversed(path[i + 1 : j + 1])
        rnd += 1
    return path


def nn_tour(indices: list[int], coords: list[tuple[float, float]], start: int) -> list[int]:
    unvisited = set(indices)
    unvisited.remove(start)
    tour = [start]
    while unvisited:
        last = tour[-1]
        nxt = min(unvisited, key=lambda j: dist_sq(coords[last], coords[j]))
        tour.append(nxt)
        unvisited.remove(nxt)
    return tour


def best_tour_for_cluster(indices: list[int], coords: list[tuple[float, float]]) -> list[int]:
    if len(indices) <= 1:
        return list(indices)
    pts = list(indices)
    # 여러 출발점에서 NN 후 2-opt, 최단 채택
    best: list[int] | None = None
    best_len = float("inf")
    cand = [pts[0], pts[len(pts) // 2], pts[-1]]
    seen = set()
    for st in cand:
        if st in seen:
            continue
        seen.add(st)
        t = nn_tour(pts, coords, st)
        t = two_opt_cycle(t, coords)
        L = tour_length(t, coords)
        if L < best_len:
            best_len = L
            best = t
    return best if best is not None else pts


def kmeans_plus_plus(
    coords: list[tuple[float, float]], k: int, iters: int = 25, rng: random.Random | None = None,
) -> list[int]:
    n = len(coords)
    rng = rng or random.Random(0)
    centroids = [coords[rng.randrange(n)]]
    d2 = [float("inf")] * n
    for _ in range(k - 1):
        for i in range(n):
            d2[i] = min(d2[i], dist_sq(coords[i], centroids[-1]))
        s = sum(d2)
        if s <= 0:
            centroids.append(coords[rng.randrange(n)])
            continue
        r = rng.random() * s
        acc = 0.0
        pick = 0
        for i in range(n):
            acc += d2[i]
            if acc >= r:
                pick = i
                break
        centroids.append(coords[pick])
        d2[pick] = 0.0
    assign = [0] * n
    for _ in range(iters):
        for i in range(n):
            best = 0
            best_d = dist_sq(coords[i], centroids[0])
            for j in range(1, k):
                d = dist_sq(coords[i], centroids[j])
                if d < best_d:
                    best_d = d
                    best = j
            assign[i] = best
        counts = [0] * k
        sx = [0.0] * k
        sy = [0.0] * k
        for i in range(n):
            c = assign[i]
            counts[c] += 1
            sx[c] += coords[i][0]
            sy[c] += coords[i][1]
        for j in range(k):
            if counts[j] > 0:
                centroids[j] = (sx[j] / counts[j], sy[j] / counts[j])
            else:
                centroids[j] = coords[rng.randrange(n)]
    return assign


def fix_empty_clusters(assign: list[int], k: int, coords: list[tuple[float, float]], rng: random.Random) -> None:
    n = len(assign)
    for _ in range(k + 5):
        sizes = [0] * k
        for c in assign:
            sizes[c] += 1
        empty = [j for j in range(k) if sizes[j] == 0]
        if not empty:
            return
        donor = max(range(k), key=lambda j: sizes[j])
        pts = [i for i in range(n) if assign[i] == donor]
        cx = sum(coords[i][0] for i in pts) / len(pts)
        cy = sum(coords[i][1] for i in pts) / len(pts)
        far = max(pts, key=lambda i: dist_sq(coords[i], (cx, cy)))
        assign[far] = empty[0]


def cluster_centroids(assign: list[int], k: int, coords: list[tuple[float, float]]) -> list[tuple[float, float]]:
    sx = [0.0] * k
    sy = [0.0] * k
    cnt = [0] * k
    for i, c in enumerate(assign):
        sx[c] += coords[i][0]
        sy[c] += coords[i][1]
        cnt[c] += 1
    out = []
    for j in range(k):
        if cnt[j] > 0:
            out.append((sx[j] / cnt[j], sy[j] / cnt[j]))
        else:
            out.append((0.0, 0.0))
    return out


def balance_by_margins(assign: list[int], k: int, coords: list[tuple[float, float]], rounds: int) -> None:
    """큰 클러스터에서 '다른 중심이 훨씬 가깝다'인 점을 작은 클러스터로 이동."""
    n = len(assign)
    target = n // k
    lo, hi = max(1, target - 2), target + 3
    for _ in range(rounds):
        sizes = [0] * k
        for c in assign:
            sizes[c] += 1
        centroids = cluster_centroids(assign, k, coords)
        big = max(range(k), key=lambda j: sizes[j])
        small = min(range(k), key=lambda j: sizes[j])
        if sizes[big] <= hi and sizes[small] >= lo:
            continue
        if sizes[big] <= sizes[small] + 1:
            continue
        pts = [i for i in range(n) if assign[i] == big]
        scored = []
        cb = centroids[big]
        for i in pts:
            db = dist_sq(coords[i], cb)
            best_j = -1
            best_dj = float("inf")
            for j in range(k):
                if j == big:
                    continue
                d = dist_sq(coords[i], centroids[j])
                if d < best_dj:
                    best_dj = d
                    best_j = j
            margin = db - best_dj
            scored.append((margin, i, best_j))
        scored.sort(reverse=True)
        moved = False
        for margin, i, j in scored[: min(50, len(scored))]:
            if margin <= 0:
                break
            if sizes[big] <= hi and sizes[small] >= lo:
                break
            if assign[i] != big:
                continue
            sizes[assign[i]] -= 1
            assign[i] = j
            sizes[j] += 1
            moved = True
            big = max(range(k), key=lambda x: sizes[x])
            small = min(range(k), key=lambda x: sizes[x])
        if not moved:
            break


def local_balance_makespan(
    assign: list[int],
    k: int,
    coords: list[tuple[float, float]],
    tours: list[list[int]],
    lengths: list[float],
    iters: int,
) -> None:
    """최대 경로 클러스터에서 점을 최소 경로 쪽으로 옮겨 max 길이를 줄임."""
    n = len(assign)
    clusters: list[list[int]] = [[] for _ in range(k)]
    for i in range(n):
        clusters[assign[i]].append(i)

    for _ in range(iters):
        cur_max = max(lengths)
        kmax = max(range(k), key=lambda j: lengths[j])
        kmin = min(range(k), key=lambda j: lengths[j])
        if lengths[kmax] <= lengths[kmin] + 1e-9:
            break
        if len(clusters[kmax]) <= 1:
            break
        centroids = cluster_centroids(assign, k, coords)
        cands = list(clusters[kmax])
        cands.sort(key=lambda i: dist_sq(coords[i], centroids[kmin]) - dist_sq(coords[i], centroids[kmax]))
        best_delta = 0.0
        best_move: tuple[int, list[int], list[int], float, float] | None = None

        for i in cands[: min(40, len(cands))]:
            new_max = clusters[kmax][:]
            new_max.remove(i)
            new_min = clusters[kmin] + [i]
            if not new_max:
                continue
            t1 = best_tour_for_cluster(new_max, coords)
            t2 = best_tour_for_cluster(new_min, coords)
            l1 = tour_length(t1, coords)
            l2 = tour_length(t2, coords)
            others = [lengths[j] for j in range(k) if j not in (kmax, kmin)]
            new_top = max(others + [l1, l2])
            if new_top < cur_max - 1e-9 and (cur_max - new_top) > best_delta:
                best_delta = cur_max - new_top
                best_move = (i, t1, t2, l1, l2)

        if best_move is None:
            break
        i, t1, t2, l1, l2 = best_move
        clusters[kmax].remove(i)
        clusters[kmin].append(i)
        assign[i] = kmin
        tours[kmax] = t1
        tours[kmin] = t2
        lengths[kmax] = l1
        lengths[kmin] = l2


def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if len(data) < 2:
        return
    it = iter(data)
    n = next(it)
    k = next(it)
    coords: list[tuple[float, float]] = []
    for _ in range(n):
        x = float(next(it))
        y = float(next(it))
        coords.append((x, y))

    rng = random.Random(42)
    assign = kmeans_plus_plus(coords, k, iters=28, rng=rng)
    fix_empty_clusters(assign, k, coords, rng)
    balance_by_margins(assign, k, coords, rounds=min(400, n))
    fix_empty_clusters(assign, k, coords, rng)

    clusters: list[list[int]] = [[] for _ in range(k)]
    for i in range(n):
        clusters[assign[i]].append(i)

    tours: list[list[int]] = []
    lengths: list[float] = []
    for j in range(k):
        t = best_tour_for_cluster(clusters[j], coords)
        tours.append(t)
        lengths.append(tour_length(t, coords))

    local_balance_makespan(assign, k, coords, tours, lengths, iters=min(25, n // 100 + 5))

    out_lines: list[str] = []
    used = [False] * n
    for j in range(k):
        t = tours[j]
        for v in t:
            used[v] = True
        line = [str(len(t))] + [str(v + 1) for v in t]
        out_lines.append(" ".join(line))

    if not all(used):
        clusters = [[] for _ in range(k)]
        for i in range(n):
            clusters[assign[i]].append(i)
        fix_empty_clusters(assign, k, coords, rng)
        clusters = [[] for _ in range(k)]
        for i in range(n):
            clusters[assign[i]].append(i)
        tours = [best_tour_for_cluster(clusters[j], coords) for j in range(k)]
        out_lines = []
        for j in range(k):
            t = tours[j]
            line = [str(len(t))] + [str(v + 1) for v in t]
            out_lines.append(" ".join(line))

    sys.stdout.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    main()
