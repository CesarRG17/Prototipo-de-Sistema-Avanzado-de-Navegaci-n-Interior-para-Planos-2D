from typing import List, Tuple
import math
 
Point = Tuple[float, float]
 
def _perp_dist(p: Point, a: Point, b: Point) -> float:
    (x0, y0), (x1, y1), (x2, y2) = p, a, b
    num = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
    den = math.hypot(y2-y1, x2-x1)
    return 0.0 if den == 0.0 else num / den
 
def rdp(points: List[Point], epsilon: float) -> List[Point]:
    if len(points) < 3:
        return points
    a, b    = points[0], points[-1]
    dmax, idx = -1.0, -1
    for i in range(1, len(points) - 1):
        d = _perp_dist(points[i], a, b)
        if d > dmax:
            dmax, idx = d, i
    if dmax <= epsilon:
        return [a, b]
    left  = rdp(points[:idx+1], epsilon)
    right = rdp(points[idx:],   epsilon)
    return left[:-1] + right