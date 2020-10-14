from matplotlib import pyplot as plt
from scipy.spatial import distance
from scipy.cluster import hierarchy
import numpy as np
import networkx as nx
from collections import defaultdict
from graph_utils import remove_top_ebet
from graph_utils import plot_graph
import community

plt.rcParams["figure.figsize"] = (20, 20)


def agglomerative_hierarchical(graph, thresh=2.4, k=None, width=1, size=500):
    "More threshold -> less clusters"
    ## Set-up the distance matrix D
    labels = list(graph.nodes())
    path_length = nx.all_pairs_shortest_path_length(graph)

    distances = np.zeros((len(graph), len(graph)))
    for u, p in path_length:
        for v, d in p.items():
            distances[list(graph.nodes()).index(u)][list(graph.nodes()).index(v)] = d
            distances[list(graph.nodes()).index(v)][list(graph.nodes()).index(u)] = d
            if u == v:
                distances[list(graph.nodes()).index(u)][
                    list(graph.nodes()).index(u)
                ] = 0

    # Create hierarchical cluster (HC)
    # There are various other routines for agglomerative clustering,
    # but here we create the HCs using the complete/max/farthest point linkage
    Y = distance.squareform(distances)  ## the upper triangular of the distance matrix
    Z = hierarchy.average(Y)

    # The partition selection (t)
    membership = list(hierarchy.fcluster(Z, t=thresh, criterion="distance"))

    # Create collection of lists for blockmodel
    partition = defaultdict(list)
    for n, p in zip(list(range(len(graph))), membership):
        partition[p].append(labels[n])

    partition = {}
    for i in range(len(membership)):
        partition[i] = membership[i]

    print(len(set(partition.values())), "clusters")

    plt.figure(figsize=(10, 10))
    plt.axis("off")

    pos = nx.spring_layout(graph, k=0.5, seed=0)

    nx.draw_networkx_nodes(
        graph, pos, cmap=plt.cm.RdYlBu, node_color=list(partition.values())
    )
    nx.draw_networkx_edges(graph, pos, alpha=0.3)
    nx.draw_networkx_labels(graph, pos)
    plt.show()

    hierarchy.dendrogram(Z)
    plt.show()