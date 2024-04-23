import unittest
from Graph import Graph, EdgeSetGraph as GraphES, AdjacencySetGraph as GraphAS


class GraphTestFactory:
    # Use setUp to create graphs for testing
    def setUp(self, GraphDS):
        # Setup vertices and edges for a few graphs to trest with
        self.g1 = GraphDS(['A', 'B', 'C', 'D', 'E'], [('A', 'B'), ('B', 'C'), ('C', 'A'), ('D', 'E'), ('E', 'C')])
        self.g2 = GraphDS(['A', 'B', 'C', 'D', 'E', 'F'], [('A', 'B'), ('A', 'C'), ('B', 'C'), ('D', 'E'), ('D', 'F'), ('E', 'F')])
        self.g_empty = GraphDS()

    def test_init(self):
        g1_results = list(self.g1)
        g2_results = list(self.g2)
        for i in ['A', 'B', 'C', 'D', 'E']:
            self.assertIn(i, g1_results)
        for j in ['A', 'B', 'C', 'D', 'E', 'F']:
            self.assertIn(j, g2_results)

        expected_neighbors = {'A': ('B', 'C'), 'B': ('A', 'C'), 'C': ('B', 'A', 'E'), 'D': tuple('E'), 'E': ('C', 'D')}
        for ver in self.g1:
            self.assertTrue(self.compare_tuples(tuple(self.g1.nbrs(ver)), expected_neighbors[ver]))

    def test_add(self):
        vertexes = ['A', 'B', 'C', 'D', 'E']
        edges = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'E'), ('D', 'E')]
        for v in vertexes:
            self.g_empty.add_vertex(v)
        for e in edges:
            self.g_empty.add_edge(e)
        ge_results = list(self.g_empty)
        for i in ['A', 'B', 'C', 'D', 'E']:
            self.assertIn(i, ge_results)

        expected_neighbors = {'A': ('B', 'C'), 'B': ('A', 'C'), 'C': ('B', 'A', 'E'), 'D': tuple('E'), 'E': ('C', 'D')}
        for ver in self.g1:
            self.assertTrue(self.compare_tuples(tuple(self.g_empty.nbrs(ver)), expected_neighbors[ver]))

    def test_connection(self):
        #every vertex in g1 is connected, so we can test every single vertex
        for ver in self.g1:
            for conn in self.g1:
                self.assertTrue(self.g1.is_connected(ver, conn))
        self.assertFalse(self.g2.is_connected('A', 'D'))
        self.assertFalse(self.g2.is_connected('B', 'E'))
        self.assertTrue(self.g2.is_connected('E', 'F'))

    def test_bfs(self):
        dist_map = {'A': 0, 'B': 1, 'C': 1, 'D': 3, 'E': 2}
        tree, dist = self.g1.bfs('A')
        for key, value in tree.items():
            self.assertEqual(value, dist_map[key])

    def test_count_trees(self):
        result1 = self.g1.count_trees()
        result2 = self.g2.count_trees()
        self.assertEqual(len(result1), 1)
        self.assertEqual(len(result2), 2)

    @staticmethod
    def compare_tuples(t1, t2) -> bool:
        return set(t1) == set(t2)


class TestAdjacency(unittest.TestCase, GraphTestFactory):
    def setUp(self):
        return GraphTestFactory.setUp(self, GraphDS=GraphAS)


class TestEdge(unittest.TestCase, GraphTestFactory):
    def setUp(self):
        return GraphTestFactory.setUp(self, GraphDS=GraphES)


if __name__ == '__main__':
    unittest.main()
