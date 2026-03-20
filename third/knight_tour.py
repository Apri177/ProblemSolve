"""
N×N 체스판에서 나이트가 모든 칸을 정확히 한 번씩 방문하는 경로(Hamiltonian path).
6 ≤ N ≤ 666, 시작 좌표가 주어짐. 좌표는 1-based로 읽고 출력한다.
해가 없으면 첫 줄에 -1 -1만 출력.
"""
import random
import sys
from typing import List, Optional, Tuple

input = sys.stdin.readline

DELTAS = (
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
)


def in_board(x: int, y: int, n: int) -> bool:
    return 0 <= x < n and 0 <= y < n


def onward_degree(x: int, y: int, board: list, n: int) -> int:
    c = 0
    for dx, dy in DELTAS:
        nx, ny = x + dx, y + dy
        if in_board(nx, ny, n) and board[nx][ny] < 0:
            c += 1
    return c


def ordered_moves(x: int, y: int, board: list, n: int, rng: random.Random) -> list:
    cand = []
    for dx, dy in DELTAS:
        nx, ny = x + dx, y + dy
        if in_board(nx, ny, n) and board[nx][ny] < 0:
            w = onward_degree(nx, ny, board, n)
            # 동점이면 보드 중심에서 멀수록 우선(경계 쪽으로 밀어 막힘 감소)
            dist = abs(nx - (n - 1) / 2) + abs(ny - (n - 1) / 2)
            cand.append((w, -dist, nx, ny))
    cand.sort(key=lambda t: (t[0], t[1]))
    # 동일 w, dist 그룹 내에서 무작위 순서
    i = 0
    out = []
    while i < len(cand):
        j = i + 1
        while j < len(cand) and cand[j][0] == cand[i][0] and cand[j][1] == cand[i][1]:
            j += 1
        chunk = [(c[2], c[3]) for c in cand[i:j]]
        rng.shuffle(chunk)
        out.extend(chunk)
        i = j
    return out


def warnsdorff_tour(n: int, sx: int, sy: int, rng: random.Random) -> Optional[List[Tuple[int, int]]]:
    total = n * n
    board = [[-1] * n for _ in range(n)]
    path = [(sx, sy)]
    board[sx][sy] = 0
    x, y = sx, sy
    for step in range(1, total):
        moves = ordered_moves(x, y, board, n, rng)
        if not moves:
            return None
        nx, ny = moves[0]
        board[nx][ny] = step
        path.append((nx, ny))
        x, y = nx, ny
    return path


def dfs_tour(
    n: int,
    x: int,
    y: int,
    board: list,
    path: list,
    depth: int,
    total: int,
) -> bool:
    if depth == total:
        return True
    moves = []
    for dx, dy in DELTAS:
        nx, ny = x + dx, y + dy
        if in_board(nx, ny, n) and board[nx][ny] < 0:
            w = onward_degree(nx, ny, board, n)
            dist = abs(nx - (n - 1) / 2) + abs(ny - (n - 1) / 2)
            moves.append((w, -dist, nx, ny))
    moves.sort(key=lambda t: (t[0], t[1]))
    for _, _, nx, ny in moves:
        board[nx][ny] = depth
        path.append((nx, ny))
        if dfs_tour(n, nx, ny, board, path, depth + 1, total):
            return True
        path.pop()
        board[nx][ny] = -1
    return False


def solve_small(n: int, sx: int, sy: int) -> Optional[List[Tuple[int, int]]]:
    total = n * n
    board = [[-1] * n for _ in range(n)]
    path = [(sx, sy)]
    board[sx][sy] = 0
    sys.setrecursionlimit(max(10000, total * 10))
    if dfs_tour(n, sx, sy, board, path, 1, total):
        return path
    return None


def main() -> None:
    n = int(input())
    sx, sy = map(int, input().split())
    sx -= 1
    sy -= 1

    if not in_board(sx, sy, n):
        print(-1, -1)
        return

    total = n * n
    # 6×6 이하만 백트래킹(시간 안전). 그보다 크면 완전 탐색 비용이 과도함.
    if total <= 36:
        ans = solve_small(n, sx, sy)
        if ans:
            for x, y in ans:
                print(x + 1, y + 1)
        else:
            print(-1, -1)
        return

    # 그 외: Warnsdorff 휴리스틱 + 동점 무작위로 여러 번 시도
    for seed in range(5000):
        rng = random.Random(seed)
        ans = warnsdorff_tour(n, sx, sy, rng)
        if ans is not None:
            for x, y in ans:
                print(x + 1, y + 1)
            return
    print(-1, -1)


if __name__ == "__main__":
    main()
