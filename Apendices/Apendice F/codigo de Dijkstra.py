import heapq
from typing import Dict, List, Tuple, Optional
 
Node  = Tuple[int, int]
Graph = Dict[Node, List[Tuple[Node, float]]]
 
def dijkstra(graph: Graph,
             start: Node,
             goal:  Optional[Node] = None):
    dist: Dict[Node, float]          = {start: 0.0}
    prev: Dict[Node, Optional[Node]] = {start: None}
    pq:   List[Tuple[float, Node]]   = [(0.0, start)]
 
    while pq:
        du, u = heapq.heappop(pq)
        if du != dist.get(u, float("inf")):
            continue
        if goal is not None and u == goal:
            break
        for v, w_uv in graph.get(u, []):
            alt = du + w_uv
            if alt < dist.get(v, float("inf")):
                dist[v] = alt
                prev[v] = u
                heapq.heappush(pq, (alt, v))
 
    return dist, prev
 
def reconstruct_path(prev:  Dict[Node, Optional[Node]],
                     start: Node,
                     goal:  Node) -> List[Node]:
    path, cur = [], goal
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    return path if path and path[0] == start else []