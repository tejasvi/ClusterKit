"""Helper functions for file I/O"""

import networkx as nx

def read_mtx(path):
    """
    Give the path of the graph in mtx format, return hashmap of node
    connections in form of dictionary.
    """

    with open(path, 'rb') as f:
        comment = 1
        while comment:
            comment = f.readline()[0] == ord('%')

        return nx.read_edgelist(f)

