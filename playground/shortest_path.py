# –––––––––– Calculates shortest path and degree of each node ––––––––––

import wntr
import networkx as nx
import matplotlib.pyplot as plt

# load water network model from an INP file
wn = wntr.network.WaterNetworkModel('networks/wntr_examples/Net3.inp')

# create graph from the water network model
G = wn.get_graph()

# draw graph using network x
plt.figure(figsize=(12, 8))
pos = {node: (wn.get_node(node).coordinates[0], wn.get_node(node).coordinates[1]) for node in wn.node_name_list}
nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=10)
plt.title("Water Distribution Network Graph")
plt.show()

# find shortest path between, e.g., node 10 and 32
start_node = '10'
end_node = '32'
shortest_path = nx.shortest_path(G, source=start_node, target=end_node)
print(f"Shortest path from node {start_node} to node {end_node}: {shortest_path}")

# print degree of each node to console
degrees = dict(G.degree())
print("Degree of each node:")
for node, degree in degrees.items():
    print(f"Node {node}: Degree {degree}")


