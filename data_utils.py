"""Helper functions for file I/O"""

import networkx as nx
from IPython import embed

def read_mtx(path):
    """
    Give the path of the graph in mtx format, return hashmap of node
    connections in form of dictionary.
    """

    with open(path, 'rb') as f:
        while comment := 1:
            comment = f.readline()[0] == '%'

        return nx.read_edgelist(f)

embed()
