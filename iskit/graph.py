import heapq
import json
import math
from collections import deque


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adj = {}

    def add_edge(self, u, v, w=1.0):
        if isinstance(w, bool) or not isinstance(w, (int, float)) or not math.isfinite(w):
            raise ValueError("Weight must be a finite number")
        if w < 0:
            raise ValueError("Negative weights are not allowed")
        for node in (u, v):
            if not isinstance(node, str):
                raise ValueError("Nodes must be strings")
            self.adj.setdefault(node, {})
        self.adj[u][v] = w
        if not self.directed:
            self.adj[v][u] = w

    def neighbors(self, u):
        return list(self.adj.get(u, {}).items())

    @classmethod
    def from_json(cls, text):
        try:
            data = json.loads(text)
            if not isinstance(data, dict) or type(data.get("directed", False)) is not bool:
                raise ValueError("Invalid graph object")
            edges = data["edges"]
            if not isinstance(edges, list):
                raise ValueError("Edges must be a list")
            graph = cls(data.get("directed", False))
            for edge in edges:
                if not isinstance(edge, list) or len(edge) not in (2, 3):
                    raise ValueError("Each edge must contain 2 or 3 values")
                graph.add_edge(edge[0], edge[1], edge[2] if len(edge) == 3 else 1.0)
            return graph
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise ValueError("Invalid graph JSON") from exc

    def bfs(self, s, goal):
        if s not in self.adj or goal not in self.adj:
            return [], 0
        queue = deque([s])
        parent = {s: None}
        expanded = 0
        while queue:
            node = queue.popleft()
            expanded += 1
            if node == goal:
                return self._path(parent, goal), expanded
            for neighbor in self.adj[node]:
                if neighbor not in parent:
                    parent[neighbor] = node
                    queue.append(neighbor)
        return [], expanded

    @staticmethod
    def _path(parent, goal):
        path = []
        while goal is not None:
            path.append(goal)
            goal = parent[goal]
        return path[::-1]

    def dijkstra(self, s, goal):
        return self._weighted_search(s, goal, lambda _: 0)

    def astar(self, s, goal, h):
        if not callable(h):
            raise TypeError("h must be callable")
        return self._weighted_search(s, goal, lambda node: h(node, goal))

    def _weighted_search(self, s, goal, heuristic):
        if s not in self.adj or goal not in self.adj:
            return [], math.inf
        counter = 0
        heap = [(0, counter, 0, s)]
        distances = {s: 0}
        parent = {s: None}
        while heap:
            _, _, cost, node = heapq.heappop(heap)
            if cost > distances[node]:
                continue
            if node == goal:
                return self._path(parent, goal), cost
            for neighbor, weight in self.neighbors(node):
                new_cost = cost + weight
                if new_cost < distances.get(neighbor, math.inf):
                    distances[neighbor] = new_cost
                    parent[neighbor] = node
                    estimate = heuristic(neighbor)
                    if isinstance(estimate, bool) or not isinstance(estimate, (int, float)) or not math.isfinite(estimate) or estimate < 0:
                        raise ValueError("Heuristic must return a finite non-negative number")
                    counter += 1
                    heapq.heappush(heap, (new_cost + estimate, counter, new_cost, neighbor))
        return [], math.inf
