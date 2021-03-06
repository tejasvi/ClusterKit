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

    print("Total ", len(set(partition.values())), "clusters detected.")

    plt.figure(figsize=(10, 10))
    plt.axis("off")

    pos = nx.spring_layout(graph, k=k, seed=0)

    plot_graph(
        graph, k=k, width=width, size=size, labels=True, color=list(partition.values())
    )
    plt.show()

    hierarchy.dendrogram(Z)
    plt.show()


def girvan_newman(graph, thresh=10, k=None, size=500, width=1):
    "More threshold does more divisions. Thresh is num of edges to remove with highest betweenness"
    graph = graph.copy()

    for i in range(thresh):
        graph = remove_top_ebet(graph)

    pos = nx.spring_layout(graph, k=k, seed=0)
    plot_graph(graph, k=k, width=width, size=size, labels=True)


def modularity(graph, thresh=1, k=None, size=500, width=1):
    "thresh indicates size of community"
    partition = community.best_partition(graph, resolution=thresh, random_state=0)
    plot_graph(
        graph=graph,
        color=list(partition.values()),
        width=width,
        size=size,
        labels=True,
        k=k,
    )