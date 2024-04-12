# Arbitrage_Graph
Creates a weighted directed graph of currencies with the respective exchange rates as their weights and uses Bellman-Ford algorithm to find the currencies available for arbitrage by finding the currencies with a negative weight cycle.



## Efficiency
The function creates the graph using Networkx runs in `O(|V| + |E|)` time complexity.
The main program and its ability to calculate the arbitrage between the currencies is predicted on the implementation of the Bellman-Ford algorithm, which runs in `O(|V| * |E|)` time complexity.



## Reasoning behind Bellman-Ford vs. Dijkstra's Algorithm
Bellman-Ford and Dijkstra's algorithms are both used to find the shortest path in a weighted graph. However, when it comes to calculating arbitrage in a weighted digraph (a directed graph where each edge has a real-valued weight as inputted based on the parsing of the provided csv file of currencies and exchange rates), Bellman-Ford is generally preferred over Dijkstra's algorithm.

Bellman-Ford can handle graphs with negative edge weights, while Dijkstra's algorithm cannot. In financial scenarios, negative weights can represent situations like losses or costs. In arbitrage detection, it's essential to consider the possibility of negative weight cycles, which indicate profitable opportunities. Bellman-Ford can effectively identify such cycles, making it more suitable for arbitrage calculations, as compared to Dijkstra's Algorithm, which cannot.



## Sequence
1. Find all distinct currencies - create a hashset of the first column of the .csv file and convert it into an array `list(set(...))`
2. Graph Initalization - done by parsing through the inputted .csv file of currencies and their corresponding exchange rates
3. Create the edges and vertices for the graph display - iterate over each row of the .csv file and ad each column as a separate element in the `.add_edge(node1, node2, weight)` function
4. Calculate the arbitrage of the graph - call `.arbitrage()` on the instantiated graph object to run the Bellman-Ford algorithm
5. Display the graph - call `.display_networkx_graph()` to call the graph created in step 3
