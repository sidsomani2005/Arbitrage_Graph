import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import heapq

class Graph:
    def __init__(self, currencies):
        self.currencies = currencies
        self.num_currencies = len(currencies)
        self.graph = [[0 for _ in range(self.num_currencies)] for _ in range(self.num_currencies)]

    def add_edge(self, source, destination, weight):
        source_index = self.currencies.index(source)
        dest_index = self.currencies.index(destination)
        self.graph[source_index][dest_index] = weight

    # def bellman_ford(self, source):
    #     dist = [float('inf')] * self.num_currencies
    #     pred = [-1] * self.num_currencies
    #     dist[source] = 0

    #     for _ in range(self.num_currencies - 1):
    #         for u in range(self.num_currencies):
    #             for v in range(self.num_currencies):
    #                 if dist[v] > dist[u] + self.graph[u][v]:
    #                     dist[v] = dist[u] + self.graph[u][v]
    #                     pred[v] = u

    #     for u in range(self.num_currencies):
    #         for v in range(self.num_currencies):
    #             if dist[v] > dist[u] + self.graph[u][v]:
    #                 return pred, u, v


    def dijkstra(self, source):
        dist = [float('inf')] * self.num_currencies
        pred = [-1] * self.num_currencies
        visited = [False] * self.num_currencies
        dist[source] = 0

        pq = [(0, source)]

        while pq:
            cost, u = heapq.heappop(pq)
            if visited[u]:
                continue
            visited[u] = True
            for v in range(self.num_currencies):
                if self.graph[u][v] > 0:  # Consider only positive weights - does not account for negative weights (need to use bellman ford algorithm for negative weights)
                    new_cost = dist[u] + self.graph[u][v]
                    if new_cost < dist[v]:
                        dist[v] = new_cost
                        pred[v] = u
                        heapq.heappush(pq, (dist[v], v))

        return pred


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


    def print_path(self, pred, start, end):
        path = []
        at = end
        while at != start:
            path.append(at)
            at = pred[at]
        path.append(start)
        path.reverse()
        print("Arbitrage Opportunity:")
        for node in path:
            print(self.currencies[node])


if __name__ == "__main__":
    data = pd.read_csv("exchange_rates.csv")
    currencies = list(set(data.iloc[:, 0]))

    exchange_graph = Graph(currencies)

    for index, row in data.iterrows():
        exchange_graph.add_edge(row[0], row[1], row[2])

    exchange_graph.display_networkx_graph()

    pred = exchange_graph.dijkstra(0)
    exchange_graph.print_path(pred, 0, 1) 

