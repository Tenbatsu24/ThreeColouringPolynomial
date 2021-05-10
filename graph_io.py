"""
Includes functions for reading and writing graphs, in a very simple readable format.
"""

import sys
from typing import IO, List, Union

from graph import Graph

DEFAULT_COLOR_SCHEME = "set13"
NUM_COLORS = 4


def read_line(f: IO[str]) -> str:
    """
    Read a single non-comment line from a file
    :param f: The file
    :return: the line
    """
    line = f.readline()

    while len(line) > 0 and line[0] == '#':
        line = f.readline()

    return line


def read_graph(graphclass, f: IO[str]) -> tuple[Graph, bool]:
    """
    Read a graph from a file
    :param graphclass: The class of the graph
    :param f: The file
    :return: The graph
    """
    options = []

    while True:
        try:
            line = read_line(f)
            n = int(line)
            graph = graphclass(n)
            break
        except ValueError:
            if len(line) > 0 and line[-1] == '\n':
                options.append(line[:-1])
            else:
                options.append(line)

    line = read_line(f)

    try:
        while True:
            comma = line.find(',')
            graph.add_edge(int(line[:comma]), int(line[comma + 1:]))
            line = read_line(f)
    except Exception:
        pass

    if line != '' and line[0] == '-':
        return graph, True
    else:
        return graph, False


def read_graph_list(graph_class, f: IO[str]) -> list[Graph]:
    """
    Read a list of graphs from a file
    :param graph_class: The graph class
    :param f: The file
    :return: A list of graphs
    """
    graphs = []
    cont = True

    while cont:
        graph, cont = read_graph(graph_class, f)
        graphs.append(graph)

    return graphs


def load_graph(f: IO[str], graph_class=Graph) -> list[Graph]:
    """
    Load a graph from a file
    :param f: The file
    :param graph_class: The class of the graph. You may subclass the default graph class and add your own here.
    :return: The graph, or a list of graphs.
    """
    return read_graph_list(graph_class, f)


def input_graph(graph_class=Graph) -> list[Graph]:
    """
    Load a graph from sys.stdin
    :param graph_class: The class of the graph. You may subclass the default graph class and add your own here.
    :return: The graph, or a list of graphs.
    """
    return load_graph(f=sys.stdin, graph_class=graph_class)


def write_line(f: IO[str], line: str):
    """
    Write a line to a file
    :param f: The file
    :param line: The line
    """
    f.write(line + '\n')


def write_graph_list(graph_list: List[Graph], f: IO[str]):
    """
    Write a graph list to a file.
    :param graph_list: The list of graphs
    :param f: the file
    """

    for i, g in enumerate(graph_list):
        n = len(g)
        write_line(f, '# Number of vertices:')
        write_line(f, str(n))

        # Give the vertices (temporary) labels from 0 to n-1:
        label = {}
        for vertex_index, vertex in enumerate(g):
            label[vertex] = vertex_index

        write_line(f, '# Edge list:')

        for e in g.edges:
            write_line(f, str(label[e.tail]) + ',' + str(label[e.head]))

        if i + 1 < len(graph_list):
            write_line(f, '--- Next graph:')


def save_graph(graph_list: Union[Graph, List[Graph]], f: IO[str]):
    """
    Write a graph, or a list of graphs to a file.
    :param graph_list: The graph, or a list of graphs.
    :param f: The file
    """
    if type(graph_list) is list:
        write_graph_list(graph_list, f)
    else:
        write_graph_list([graph_list], f)


def print_graph(graph_list: Union[Graph, List[Graph]]):
    """
    Print a graph, or a list of graphs to sys.stdout
    :param graph_list: The graph, or list of graphs.
    """
    if type(graph_list) is list:
        write_graph_list(graph_list, sys.stdout)
    else:
        write_graph_list([graph_list], sys.stdout)


def write_dot(graph: Graph, f: IO[str], directed=False):
    """
    Writes a given graph to a file in .dot format.
    :param graph: The graph. If its vertices contain attributes `label`, `colortext` or `colornum`, these are also
    included in the file. If its edges contain an attribute `weight`, these are also included in the file.
    :param f: The file.
    :param directed: Whether the graph should be drawn as a directed graph.
    """
    if directed:
        f.write('digraph G {\n')
    else:
        f.write('graph G {\n')

    name = {}
    next_name = 0

    for v in graph:
        name[v] = next_name
        next_name += 1
        options = 'penwidth=3,'

        if hasattr(v, 'label'):
            options += 'label="' + str(v.label) + '",'

        if hasattr(v, 'colour'):
            options += 'color=' + str(v.colour % NUM_COLORS) + ', colorscheme=' + DEFAULT_COLOR_SCHEME + ','
            if v.colour >= NUM_COLORS:
                options += 'style=filled,fillcolor=' + str((v.colour // NUM_COLORS) % NUM_COLORS) + ','
        if len(options) > 0:
            f.write('    ' + str(name[v]) + ' [' + options[:-1] + ']\n')
        else:
            f.write('    ' + str(name[v]) + '\n')
    f.write('\n')

    for e in graph.edges():
        options = ','
        if len(options) > 0:
            options = '[penwidth=2]'
        if directed:
            f.write('    ' + str(name[e.tail]) + ' -> ' + str(name[e.head]) + options + '\n')
        else:
            f.write('    ' + str(name[e.tail]) + '--' + str(name[e.head]) + options + '\n')

    f.write('}')
