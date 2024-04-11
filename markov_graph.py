import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from math import log


class Graph:

    def __init__(self, currencies):
        self.currencies = currencies
        self.num_currencies = len(currencies)
        self.graph = [[0 for _ in range(self.num_currencies)] for _ in range(self.num_currencies)]

    def add_edge(self, source, destination, weight):
        source_index = self.currencies.index(source)
        dest_index = self.currencies.index(destination)
        self.graph[source_index][dest_index] = weight

    def arbitrage(self):
        trans_graph = self.negate_logarithm_convertor()

        # pick any source vertex -- we can run Bellman-Ford from any vertex and get the right result
        source = 0
        n = self.num_currencies
        min_dist = [float('inf')] * n
        pre = [-1] * n
        min_dist[source] = source

        # BELLMAN-FORD ALGORITHM - O(|V|*|E|)
        for _ in range(n - 1):
            for source_curr in range(n):
                for dest_curr in range(n):
                    if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                        min_dist[dest_curr] = min_dist[source_curr] + trans_graph[source_curr][dest_curr]
                        pre[dest_curr] = source_curr

        # if we can still relax edges, then we have a negative cycle
        for source_curr in range(n):
            for dest_curr in range(n):
                if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                    # negative cycle exists, and use the predecessor chain to print the cycle
                    print_cycle = [dest_curr, source_curr]
                    # start from the source and go backwards until you see the source vertex again or any vertex that already exists in print_cycle array
                    while pre[source_curr] not in print_cycle:
                        print_cycle.append(pre[source_curr])
                        source_curr = pre[source_curr]
                    print_cycle.append(pre[source_curr])
                    print()
                    print()
                    print("ARBITRAGE OPPORTUNITY: \n")
                    print(" --> ".join([self.currencies[p] for p in print_cycle[::-1]]))
                    return

        print()
        print("No arbitrage opportunity found.")

    def negate_logarithm_convertor(self):
        ''' log of each rate in graph and negate it'''
        result = []
        for row in self.graph:
            negated_row = []
            for edge in row:
                negated_row.append(-log(edge))
            result.append(negated_row)
        return result

    def display_networkx_graph(self):
        G = nx.DiGraph()

        for i, source in enumerate(self.currencies):
            for j, destination in enumerate(self.currencies):
                G.add_edge(source, destination, weight=self.graph[i][j])

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, font_size=8)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5)

        plt.show()


if __name__ == "__main__":
    data = pd.read_csv("exchange_rates_negative.csv")
    currencies = list(set(data.iloc[:, 0]))
    print("Unique destination currencies:", currencies) 

    exchange_graph = Graph(currencies)

    for index, row in data.iterrows():
        print("Adding edge:", row[0], "->", row[1], "with weight", row[2])
        exchange_graph.add_edge(row[0], row[1], row[2])

    exchange_graph.arbitrage()
    exchange_graph.display_networkx_graph()
    
