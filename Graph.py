from queue import Queue
from collections import deque

class Graph:
    def __init__(self, V, E):
        raise NotImplementedError('Graph is a utility class and should not be initialized!')

    def is_connected(self, v1, v2):
        return self._connected(v1, v2, set())

    def _connected(self, v1, v2, visited):
        if v1 in visited or not self.nbrs(v1):
            return False
        if v2 == v1:
            return True
        visited.add(v1)
        return any(self._connected(n, v2, visited) for n in self.nbrs(v1))



    def bfs(self, v):
        tree = {}
        tovisit = Queue()
        tovisit.put((None, v))
        visited = 0
        while tovisit.empty():
            a, b = tovisit.get()
            visited += 1
            if b not in tree:
                tree[b] = a
                for n in self.nbrs(b):
                    tovisit.put((b, n))
        return tree, visited

    def count_trees(self):
        visited = set()
        trees = []

        for start_node in self.__iter__():
            if start_node not in visited:
                queue = deque([(start_node, None, True)])

                tree = {}
                while queue:
                    node, parent, first_child = queue.pop()

                    if first_child:
                        tree[node] = parent

                    visited.add(node)
                    first_child_flag = True

                    for neighbor in self.nbrs(node):
                        if neighbor == node or neighbor in visited:
                            continue

                        queue.append((neighbor, node, first_child_flag))
                        first_child_flag = False

                trees.append(tree)
        return trees


class AdjacencySetGraph(Graph):

    def __init__(self, V=None, E=None):
        self.vertices = set()
        self.edges = {}
        if E is not None:
            for edge in E:
                self.add_edge(edge)
        if V is not None:
            for v in V:
                self.add_vertex(v)

    def __len__(self):
        return len(self.vertices)

    def __iter__(self):
        return iter(self.vertices)

    def add_vertex(self, v):
        self.vertices.add(v)

    def remove_vertex(self, v):
        if v not in self.vertices:
            raise KeyError(f'Vertex {v} is not in the graph!')
        self.vertices.remove(v)

    def add_edge(self, e):
        e1, e2 = e

        if e1 not in self.edges:
            self.edges[e1] = {e2}
        else:
            self.edges[e1].add(e2)

        if e2 not in self.edges:
            self.edges[e2] = {e1}
        else:
            self.edges[e2].add(e1)

    def remove_edge(self, e):
        e1, e2 = e

        if e2 not in self.edges[e1]:
            raise KeyError(f'{e2} not connected to {e1}!')
        if e1 not in self.edges[e2]:
            raise KeyError(f'{e1} not connected to {e2}!')

        self.edges[e1].remove(e2)
        self.edges[e2].remove(e1)

    def nbrs(self, v):
        if v not in self.edges:
            return None
        return iter(self.edges[v])


class EdgeSetGraph(Graph):

    def __init__(self, V=None, E=None):
        self.vertices = set()
        self.edges = set()
        if E is not None:
            for edge in E:
                self.add_edge(edge)
        if V is not None:
            for v in V:
                self.add_vertex(v)

    def __len__(self):
        return len(self.vertices)

    def __iter__(self):
        return iter(self.vertices)

    def add_vertex(self, v):
        self.vertices.add(v)

    def remove_vertex(self, v):
        if v not in self.vertices:
            raise KeyError(f'Vertex {v} is not in the graph!')
        self.vertices.remove(v)

    def add_edge(self, e):
        frozen_edge = frozenset(e)
        self.edges.add(frozen_edge)

    def remove_edge(self, e):
        frozen_edge = frozenset(e)
        self.edges.remove(frozen_edge)

    def nbrs(self, v):
        for pair in self.edges:
            v1, v2 = pair
            if v1 == v:
                yield v2
            if v2 == v:
                yield v1
