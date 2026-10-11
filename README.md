# Reusable Graph Toolkit

Python 3.9+; no external dependencies.

## Run tests
From the project root:

```bash
python -m unittest discover -s tests -v
```

## Example
```python
from iskit.graph import Graph

g = Graph.from_json('{"directed": false, "edges": [["A","B",2],["B","C",3],["A","C",10]]}')
print(g.neighbors("A"))
print(g.bfs("A", "C"))            # (["A", "C"], expanded_nodes)
print(g.dijkstra("A", "C"))       # (["A", "B", "C"], 5)
print(g.astar("A", "C", lambda node, goal: 0))  # (["A", "B", "C"], 5)
```

BFS finds a path with the fewest edges and returns `(path, expanded_nodes)`.
Dijkstra and A* return `(path, total_cost)`. Unreachable weighted goals return `([], math.inf)`.
A* requires a non-negative admissible heuristic for optimality; zero is equivalent to Dijkstra.
Nodes are strings. Edges default to weight 1. Negative, non-finite, or nonnumeric weights are rejected.

## Git
```bash
git init
git add iskit
git commit -m "Implement adjacency graph and JSON loading"
git add tests
git commit -m "Add algorithm and edge-case tests"
git add README.md
git commit -m "Document usage and test instructions"
```
Create your own remote repository and push the commits. A repository link must be supplied separately.
