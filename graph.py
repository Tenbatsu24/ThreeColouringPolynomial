class Edge:

    def __init__(self, tail, head):
        self.tail = tail
        self.head = head


class Vertex:

    def __init__(self, name, graph):
        self.label = name
        self.colour = 0
        self.belongs_to = graph
        self.neighbours = set()

    def add_neighbour(self, neighbour):
        self.neighbours.add(neighbour)

    def __iter__(self):
        return iter(self.neighbours)


class Graph:

    def __init__(self, n):
        self.v_count = n
        self.__vs = [Vertex(i, self) for i in range(n)]
        self.__es = []

    def add_edge(self, u, v):
        head = self.__vs[u]
        tail = self.__vs[v]

        head.add_neighbour(tail)
        tail.add_neighbour(head)
        self.__es.append(Edge(tail, head))

    def edges(self):
        return iter(self.__es)

    def __getitem__(self, item):
        return self.__vs[item]

    def __iter__(self):
        return iter(self.__vs)

    def __len__(self):
        return self.v_count
