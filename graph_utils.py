"""Helper functions for graph analysis"""

import networkx as nx
import networkx.algorithms.community as nx_comm
import collections
from matplotlib import pyplot as plt
import operator

plt.rcParams["figure.figsize"] = (20, 20)


def plot_graph(graph, k=None, width=0.1, labels=False, size=1, color="r"):
    nx.draw_networkx(
        graph,
        pos=nx.spring_layout(graph, k=k, seed=0),
        arrows=False,
        with_labels=labels,
        node_size=size,
        width=width,
        node_color=color,
    )


def highlight_nodes(graph, nodes, k=None):
    plot_graph(graph, k=k)
    nx.draw_networkx(
        graph.subgraph(nodes),
        pos=nx.spring_layout(graph, k=k, seed=0),
        font_size=16,
        node_color="red",
        font_color="green",
    )
    plt.show()


def graph_info(graph, print_info=True):
    info = {
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "avg_degree": sum(dict(graph.degree()).values()),
        "clustering_coef": round(nx.average_clustering(graph), 3),
    }
    info["avg_degree"] = round(info["avg_degree"] / info["num_nodes"], 3)

    if print_info:
        for k, v in info.items():
            print("".join(k.replace("_", " ")).capitalize() + ": ", v)

    return info


get_modularity = nx_comm.modularity


def plot_degree_distribution(graph):
    degree_sequence = sorted(
        [d for n, d in graph.degree()], reverse=True
    )  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color="b")

    plt.title("Degree Distribution")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    plt.xscale("log")
    plt.yscale("log")
    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    graphcc = graph.subgraph(
        sorted(nx.connected_components(graph), key=len, reverse=True)[0]
    )
    plt.axis("off")
    plt.show()
