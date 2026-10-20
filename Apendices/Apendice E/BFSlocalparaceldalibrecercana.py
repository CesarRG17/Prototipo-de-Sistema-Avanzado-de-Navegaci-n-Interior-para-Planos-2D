import unicodedata
from collections import deque
from typing import Tuple, List, Dict, Any

def normalize_label(s: str) -> str:
    s = s.upper().strip()
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s
                if unicodedata.category(ch) != "Mn")
    cleaned = [ch for ch in s
               if ch.isalnum() or ch in {" ", "-"}]
    s = "".join(cleaned).replace("-", "")
    return " ".join(s.split())

def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            cur[j] = min(prev[j]+1, cur[j-1]+1, prev[j-1]+cost)
        prev = cur
    return prev[-1]

def map_poi_to_free_cell(grid01, i0: int, j0: int,
                          r: int = 10,
                          use_8conn: bool = True
                          ) -> Tuple[int, int]:
    ny, nx = grid01.shape
    i0 = max(0, min(nx-1, i0))
    j0 = max(0, min(ny-1, j0))
    if grid01[j0, i0] == 0:
        return i0, j0

    neigh = ([(-1,0),(1,0),(0,-1),(0,1),
               (-1,-1),(1,-1),(-1,1),(1,1)]
             if use_8conn else
             [(-1,0),(1,0),(0,-1),(0,1)])

    visited, q = {(i0,j0)}, deque([(i0,j0)])
    while q:
        i, j = q.popleft()
        if max(abs(i-i0), abs(j-j0)) > r:
            continue
        if grid01[j, i] == 0:
            return i, j
        for di, dj in neigh:
            ni, nj = i+di, j+dj
            if (0 <= ni < nx and 0 <= nj < ny
                    and (ni, nj) not in visited):
                visited.add((ni, nj))
                q.append((ni, nj))
    return i0, j0

def best_match(query: str, pois: List[Dict[str, Any]],
               tau_sim: float = 0.75):
    qn = normalize_label(query)
    best, best_sim = None, -1.0
    for poi in pois:
        sn = normalize_label(poi["text"])
        d  = levenshtein(qn, sn)
        sim = 1.0 - d / max(len(qn), len(sn), 1)
        if sim > best_sim:
            best_sim, best = sim, poi
    if best is None or best_sim < tau_sim:
        return None, best_sim
    return best, best_sim