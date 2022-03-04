import matplotlib.pyplot as plt
import networkx as nx


def condensation():
    G = nx.read_gexf('university-network-20000.gexf', node_type=str)
    with open('condensation.txt', 'w') as f:
        g_prime = nx.condensation(G)
        g_prime1 = nx.condensation(G)

        # condense graph and remove low degree nodes
        low_degree = [node for node, degree in dict(g_prime.in_degree()).items() if degree < 2]
        print(len(low_degree))
        g_prime.remove_nodes_from(low_degree)

        print('Visualising condensed graph')
        nx.draw(g_prime)
        plt.show()

        # dedensify condensed graph
        g_prime_condensed, g_prime_condensed_nodes = nx.dedensify(g_prime1, threshold=100)
        print(len(g_prime_condensed.nodes))
        print(len(g_prime_condensed.edges))

        # dedensify original graph
        print('Dedensify')
        new_graph, new_nodes = nx.dedensify(G, threshold=100)
        print(len(new_graph.nodes))
        print(len(new_graph.edges))


if __name__ == '__main__':
    condensation()
