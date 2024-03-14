import wntr

class Network:
    ''' Manages the water distribution network model. '''
    def __init__(self, network_file):
        ''' Network object constructor '''
        self.wn = wntr.network.WaterNetworkModel(network_file)
        self.G = self.wn.get_graph().to_undirected()
        self.assign_edge_lengths()

    def assign_edge_lengths(self):
        ''' Assigns lengths to edges based on pipe lengths in the inp file. '''
        for pipe_name, pipe in self.wn.pipes():
            start_node, end_node = pipe.start_node_name, pipe.end_node_name
            length = pipe.length
            # MultiDiGraph, so may be multiple edges between two nodes...
            if self.G.has_edge(start_node, end_node):
                for key in self.G[start_node][end_node]:
                    self.G[start_node][end_node][key]['length'] = length
        
    def scale_network(self, window_width, window_height, margin):
        ''' Scales the network to fit the window. '''
        min_x = min([self.G.nodes[node]['pos'][0] for node in self.G.nodes])
        min_y = min([self.G.nodes[node]['pos'][1] for node in self.G.nodes])
        max_x = max([self.G.nodes[node]['pos'][0] for node in self.G.nodes])
        max_y = max([self.G.nodes[node]['pos'][1] for node in self.G.nodes])
        scale_x = (window_width - 2 * margin) / (max_x - min_x)
        scale_y = (window_height - 2 * margin) / (max_y - min_y)
        offset_x = -min_x * scale_x + margin
        offset_y = -min_y * scale_y + margin
        for node in self.G.nodes:
            pos = self.G.nodes[node]['pos']
            scaled_pos = (int(pos[0] * scale_x + offset_x), int(pos[1] * scale_y + offset_y))
            self.G.nodes[node]['pos'] = scaled_pos

    def get_neighbors_and_distance(self, node):
        ''' Returns neighbors and distances from a node. '''
        neighbors = list(self.G.neighbors(node))
        distances = {}
        for neighbor in neighbors:
            key = next(iter(self.G[node][neighbor]), None)
            if key is not None and 'length' in self.G[node][neighbor][key]:
                distances[neighbor] = self.G[node][neighbor][key]['length']
            else:
                # If no length found, set default value to zero then this is later ignnored
                distances[neighbor] = 0
        return neighbors, distances