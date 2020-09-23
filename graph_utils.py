"""Helper functions for graph analysis"""

import networkx as nx

from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = (20,20)

def plot_graph(graph, k=2):
    nx.draw_networkx(graph, pos=nx.spring_layout(graph, k=k, seed=0), arrows=False, with_labels=False, node_size=1, width=0.1)

def graph_info(graph):
    info = {'num_nodes': g.number_of_nodes(), 'num_edges': g.number_of_edges(), 'avg_degree': sum(dict(G.degree()).values())}
    info['avg_degree'] /= info['num_nodes']
    return info
