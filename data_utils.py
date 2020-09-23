"""Helper functions for file I/O"""

from collections import defaultdict
from IPython import embed

def read_mtx(path):
    """
    Give the path of the graph in mtx format, return hashmap of node
    connections in form of dictionary.
    """

    hashmap = defaultdict(list)
    
    with open(path, 'r') as f:
        for line in f:
            if line[0] != '%':
                str_nodes = line.split()[:2]
                node1, node2 = (int(x) for x in str_nodes)
                hashmap[node1].append(node2)
    
    return hashmap

embed()
