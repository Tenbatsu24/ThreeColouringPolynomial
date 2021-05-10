from graph import *
from graph_io import write_dot, load_graph

colour_transition = {
    1: {0: 2,
        1: 2,
        2: 2,
        3: 3},
    2: {0: 1,
        1: 1,
        2: 3,
        3: 3},
    3: {0: 1,
        1: 1,
        2: 2,
        3: 4}
}


def three_colouring_iteration(start):
    start.colour = 1
    queue, visited = {start}, {start}

    while queue:
        curr_node = queue.pop()
        parent_colour = curr_node.colour

        for neighbour in curr_node:
            assigned_colour = neighbour.colour = colour_transition[parent_colour][neighbour.colour]
            if assigned_colour == 4:
                return False
            if neighbour not in visited:
                queue.add(neighbour)
                visited.add(neighbour)
    return True


def three_colouring(graph):
    for start in graph:
        print(start.label)
        for v in graph:
            v.colour = 0

        if three_colouring_iteration(start):
            return True
    print("Graph is not 3 colourable")
    return False


def non_three_colourable():
    G = Graph(4)
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    G.add_edge(2, 0)

    G.add_edge(3, 0)
    G.add_edge(3, 1)
    G.add_edge(3, 2)

    three_colouring(G)

    # print([v.colour for v in G])
    with open('./dots/icosahedron.dot', 'w') as f:
        write_dot(G, f)


def triangle():
    H = Graph(3)
    H.add_edge(0, 1)
    H.add_edge(1, 2)
    H.add_edge(2, 0)

    three_colouring(H)
    # print([v.colour for v in H])
    with open('./dots/triangle.dot', 'w') as f:
        write_dot(H, f)


def petersen_graph():
    PetersenGraph = Graph(10)
    PetersenGraph.add_edge(0, 1)
    PetersenGraph.add_edge(0, 4)
    PetersenGraph.add_edge(0, 5)

    PetersenGraph.add_edge(1, 2)
    PetersenGraph.add_edge(1, 6)

    PetersenGraph.add_edge(2, 3)
    PetersenGraph.add_edge(2, 7)

    PetersenGraph.add_edge(3, 4)
    PetersenGraph.add_edge(3, 8)

    PetersenGraph.add_edge(4, 9)

    PetersenGraph.add_edge(5, 7)
    PetersenGraph.add_edge(5, 8)

    PetersenGraph.add_edge(6, 8)
    PetersenGraph.add_edge(6, 9)

    PetersenGraph.add_edge(7, 9)

    three_colouring(PetersenGraph)
    # print([v.colour for v in PetersenGraph])
    with open('./dots/petersen.dot', 'w') as f:
        write_dot(PetersenGraph, f)


def test_simple():
    print('icosahedron')
    non_three_colourable()
    print()
    print('triangle')
    triangle()
    print()
    print('petersen graph')
    petersen_graph()


if __name__ == '__main__':
    test_simple()

    Directory = 'basic'
    Filenames = ['colorref_smallexample_4_7', 'cref9vert_4_9', 'colorref_smallexample_4_16',
                 'colorref_smallexample_6_15', 'colorref_smallexample_2_49', 'colorref_largeexample_6_960',
                 'colorref_largeexample_4_1026', 'unique_planar']

    print()
    for filename in Filenames:
        print(filename)
        with open(f'./{Directory}/{filename}.grl', 'r') as f:
            graphs = load_graph(f, Graph)

        idx = 0
        three_colouring(graphs[idx])

        with open(f'./dots/dot_{filename}_{idx}.dot', 'w') as f:
            write_dot(graphs[0], f)
        print()
