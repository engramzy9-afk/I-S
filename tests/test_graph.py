import math
import unittest
from iskit.graph import Graph


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.g = Graph()
        self.g.add_edge("A", "B", 2)
        self.g.add_edge("B", "C", 3)
        self.g.add_edge("A", "C", 10)
        self.g.add_edge("D", "E")

    def test_undirected(self):
        self.assertIn(("A", 2), self.g.neighbors("B"))

    def test_directed(self):
        g = Graph(True)
        g.add_edge("A", "B")
        self.assertEqual(g.neighbors("B"), [])

    def test_default_weight(self):
        self.assertEqual(self.g.neighbors("D"), [("E", 1.0)])

    def test_json(self):
        g = Graph.from_json('{"directed":true,"edges":[["A","B",2],["B","C"]]}')
        self.assertEqual(g.neighbors("A"), [("B", 2)])
        self.assertEqual(g.neighbors("C"), [])

    def test_invalid_json(self):
        with self.assertRaises(ValueError):
            Graph.from_json('{"edges": [}')

    def test_invalid_json_structure(self):
        with self.assertRaises(ValueError):
            Graph.from_json('{"edges": "bad"}')

    def test_negative_weight(self):
        with self.assertRaises(ValueError):
            self.g.add_edge("X", "Y", -1)

    def test_negative_json_weight(self):
        with self.assertRaises(ValueError):
            Graph.from_json('{"edges":[["A","B",-3]]}')

    def test_bfs(self):
        self.assertEqual(self.g.bfs("A", "C")[0], ["A", "C"])

    def test_bfs_unreachable(self):
        self.assertEqual(self.g.bfs("A", "E")[0], [])

    def test_dijkstra(self):
        self.assertEqual(self.g.dijkstra("A", "C"), (["A", "B", "C"], 5))

    def test_astar(self):
        h = {"A": 4, "B": 3, "C": 0, "D": 0, "E": 0}
        self.assertEqual(self.g.astar("A", "C", lambda n, goal: h[n]), (["A", "B", "C"], 5))

    def test_weighted_unreachable(self):
        self.assertEqual(self.g.dijkstra("A", "E"), ([], math.inf))
        self.assertEqual(self.g.astar("A", "E", lambda n, goal: 0), ([], math.inf))

    def test_same_start_goal(self):
        self.assertEqual(self.g.bfs("A", "A"), (["A"], 1))
        self.assertEqual(self.g.dijkstra("A", "A"), (["A"], 0))

    def test_missing_node(self):
        self.assertEqual(self.g.bfs("Z", "A"), ([], 0))
        self.assertEqual(self.g.dijkstra("Z", "A"), ([], math.inf))

    def test_invalid_heuristic(self):
        with self.assertRaises(ValueError):
            self.g.astar("A", "C", lambda n, goal: -1)


if __name__ == "__main__":
    unittest.main()
