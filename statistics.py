import operator
from collections import Counter

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities


def get_top_n_values(centrality, num_items, reverse=True):
    sorted_dict = sorted(centrality.items(), key=operator.itemgetter(1), reverse=reverse)
    return list(sorted_dict)[:num_items]


def plot_degree(graph, with_log_scale=False):
    degree_tuple = graph.degree()
    # get frequency of degrees
    degrees = [ele[1] for ele in degree_tuple]
    degree_freq = Counter(degrees)
    # zip item and its frequency
    x, y = zip(*degree_freq.items())

    plt.figure(1)
    plt.title('Degree distribution without log scale')
    plt.xlabel('Degree')
    plt.ylabel('Count')
    if with_log_scale:
        plt.title('Degree distribution with log scale')
        plt.xscale('log')
        plt.xlim(1, max(x))
        plt.yscale('log')
        plt.ylim(1, max(y))

    plt.scatter(x, y, marker='.')
    plt.show()


def get_network_statistics():
    G = nx.read_gexf('university-network-20000.gexf', node_type=str)
    with open('network_statistics.txt', 'w') as f:
        num_nodes = len(G.nodes)
        num_edges = len(G.edges)
        density = nx.density(G)
        print(f'Number of nodes: {num_nodes}')
        print(f'Number of edges: {num_edges}')
        print(f'Edge Density: {density}')
        clustering_coeff = nx.average_clustering(G)
        print(f'Average clustering coefficient: {clustering_coeff}')
        f.write(f'Number of nodes: {num_nodes}\n')
        f.write(f'Number of edges: {num_edges}\n')
        f.write(f'Edge Density: {density}\n')
        f.write(f'Average clustering coefficient: {clustering_coeff}\n')
        plot_degree(G)
        plot_degree(G, True)

        num_scc = nx.number_strongly_connected_components(G)
        num_wcc = nx.number_weakly_connected_components(G)
        print(f'Number of SCC: {num_scc}')
        print(f'Number of WCC: {num_wcc}')
        f.write(f'Number of SCC: {num_scc}\n')
        f.write(f'Number of WCC: {num_wcc}\n')
        largest_scc = max(nx.strongly_connected_components(G), key=len)
        largest_wcc = max(nx.weakly_connected_components(G), key=len)
        num_nodes_scc = len(largest_scc)
        num_nodes_wcc = len(largest_wcc)
        print(f'Number of nodes in largest SCC: {num_nodes_scc}')
        print(f'Number of nodes in largest WCC: {num_nodes_wcc}')
        f.write(f'Number of nodes in largest SCC: {num_nodes_scc}\n')
        f.write(f'Number of nodes in largest WCC: {num_nodes_wcc}\n')
        g_scc = G.subgraph(largest_scc)
        g_wcc = G.subgraph(largest_wcc).to_undirected()
        shortest_path_length_scc = nx.average_shortest_path_length(g_scc)
        shortest_path_length_wcc = nx.average_shortest_path_length(g_wcc)
        print(f'Average shortest path length in largest SCC: {shortest_path_length_scc}')
        print(f'Average shortest path length in largest WCC: {shortest_path_length_wcc}')
        f.write(f'Average shortest path length in largest SCC: {shortest_path_length_scc}\n')
        f.write(f'Average shortest path length in largest WCC: {shortest_path_length_wcc}\n')
        scc_diameter = nx.diameter(g_scc)
        wcc_diameter = nx.diameter(g_wcc)
        print(f'Diameter of largest SCC: {scc_diameter}')
        print(f'Diameter of largest WCC: {wcc_diameter}')
        f.write(f'Diameter of largest SCC: {scc_diameter}\n')
        f.write(f'Diameter of largest WCC: {wcc_diameter}\n')

        pagerank = nx.pagerank(G)
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)
        closeness_centrality = nx.closeness_centrality(G)
        # eigenvector_centrality = nx.eigenvector_centrality(G)
        # harmonic_centrality = nx.harmonic_centrality(G)
        # subgraph_centrality = nx.subgraph_centrality(G)

        centrality_sorting(f, pagerank, 'Page Rank')
        centrality_sorting(f, degree_centrality, 'Degree Centrality')
        centrality_sorting(f, betweenness_centrality, 'Betweenness Centrality')
        centrality_sorting(f, closeness_centrality, 'Closeness Centrality')
        # centrality_sorting(f, eigenvector_centrality, 'Eigenvector Centrality')
        # centrality_sorting(f, harmonic_centrality, 'Harmonic Centrality')
        # centrality_sorting(f, subgraph_centrality, 'Subgraph Centrality')

        # gn_communities = girvan_newman(G)
        # # k is the number of communities
        # k = 20
        # limited = itertools.takewhile(lambda c: len(c) <= k, gn_communities)
        # print("Girvan-Newman community detection algorithm")
        # for community in limited:
        #     if len(community) == 20:
        #         communities = tuple(sorted(c) for c in community)
        #         i = 0
        #         for c in communities:
        #             if i < 5:
        #                 com_size = len(c)
        #                 print(com_size)
        #                 f.write(f'{com_size}\n')
        #                 f.write(f'{random.sample(c, 5)}\n')
        #                 i += 1
        #             else:
        #                 break
        #
        print("Greedy modularity maximization")

        greedy_communities = greedy_modularity_communities(G, n_communities=20)
        f.write(f'Greedy modularity maximization\n')
        i = 0
        for community in greedy_communities:
            if i < 5:
                print(f'Community{i+1}')
                com_size = len(community)
                print(com_size)
                f.write(f'{com_size}\n')
                # random sampling
                # sample_nodes = random.sample(community, 5)
                # f.write(f'{sample_nodes}\n')
                nodes = list(community)
                # sort the nodes in descending order of node degrees
                sorted_degrees = sorted(G.degree(nodes), key=lambda x: x[1], reverse=True)

                rep_nodes = sorted_degrees[:5]
                f.write(f'{rep_nodes}\n')
                i += 1
            else:
                break


def centrality_sorting(f, centrality, centrality_name):
    top_centralities = get_top_n_values(centrality, 10)
    least_centralities = get_top_n_values(centrality, 10, False)
    print(f"Writing {centrality_name}")
    f.write(f'Top {centrality_name}: {top_centralities}\n')
    f.write(f'Least {centrality_name}: {least_centralities}\n')


if __name__ == '__main__':
    get_network_statistics()
