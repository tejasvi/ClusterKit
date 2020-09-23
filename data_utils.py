"""Helper functions for file I/O"""

import networkx as nx
from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = (20,20)

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

def plot_graph(graph, k=0.5):
    nx.draw_networkx(g, pos=nx.spring_layout(g, k=k), arrows=False, with_labels=False, node_size=1, width=0.1)
