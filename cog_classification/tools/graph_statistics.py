import networkx as nx
import topology_generator as gen


"""
Calculates statistic defined in write graph for graphs from topology generator and files.
The statistics are printed as a row of table.
"""

# The number of agents for graph generator.
size = 16


def write_graph(graph_name, graph_body):
    """
    Calculate and prints statistics of graph.

    :param graph_name: name of graph.
    :type graph_name: string
    :param graph_body: the body of graph.
    :type graph_body: Graph
    """
    radius = nx.radius(graph_body)
    # https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.distance_measures.radius.html

    diameter = nx.diameter(graph_body)
    # https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.distance_measures.diameter.html

    closeness = float(sum(nx.algorithms.centrality.closeness_centrality(graph_body).values()))/size
    # https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.centrality.closeness_centrality.html#networkx.algorithms.centrality.closeness_centrality

    betweenness = float(sum(nx.algorithms.centrality.betweenness_centrality(graph_body).values()))/size
    # https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.centrality.betweenness_centrality.html#networkx.algorithms.centrality.betweenness_centrality

    clustering = float(sum(nx.algorithms.clustering(graph_body).values()))/size
    # https://networkx.github.io/documentation/latest/reference/generated/networkx.algorithms.cluster.clustering.html#networkx.algorithms.cluster.clustering

    statistics = (graph_name, radius, diameter, closeness, betweenness, clustering)

    form = "%s"
    for _ in range(len(statistics) - 1):
        form += "\t%s"

    print form % statistics


# First row of table.
statistics_names = ["Topology", "Radius", "Diameter", "Closeness", "Betweenness", "Clustering"]
print "\t".join(statistics_names)

graphs = ["clique", "line", "hub"]

for graph in graphs:
    generated_graph = nx.Graph(gen.generate_topology(graph, agents_names=range(size)))
    write_graph(graph, generated_graph)

path = "../../examples/networks/"
files = ["max_avg_bet.json",
         "max_avg_clust.json",
         "max_max_bet.json",
         "max_max_clos.json",
         "max_var_cons.json",
         "min_avg_bet.json",
         "min_avg_clust.json",
         "min_max_clos.json"]

for f in files:
    source = gen.generate_topology("file", file_name=path+f)

    graph = {}

    for node in source["nodes"]:
        graph[node] = []
        for edge in source["edges"]:
            if edge["from"] == node:
                graph[node].append(edge["to"])

    generated_graph = nx.Graph(graph)
    write_graph(f, generated_graph)
