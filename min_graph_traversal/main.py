import networkx as nx
import os

def parse_inp_pipes_section(inp_file_path):
    ''' Parses the [PIPES] section of an INP file and returns edge data. '''
    with open(inp_file_path, 'r') as file:
        lines = file.readlines()
    
    pipes_section_found = False
    edges = []
    for line in lines:
        if line.strip() == "[PIPES]":
            pipes_section_found = True
            continue
        if pipes_section_found:
            if line.strip() == "" or line.strip().startswith(";"): 
                if edges:
                    break
                else:
                    continue
            parts = line.split()
            try:
                head_node, tail_node, length = parts[1], parts[2], float(parts[3])
                edges.append((head_node, tail_node, length))
            except ValueError:
                continue
    return edges

def construct_graph(edges):
    ''' Constructs a graph from edges data. '''
    G = nx.Graph()
    for head, tail, length in edges:
        G.add_edge(head, tail, weight=length)
    return G

def approximate_min_distance(G):
    ''' Approximates the minimum total distance using a traversal algorithm. '''
    visited = set()
    total_distance = 0
    start_node = list(G.nodes)[0]
    stack = [(start_node, 0)]
    
    while stack:
        node, distance_to_node = stack.pop()
        if node not in visited:
            visited.add(node)
            total_distance += distance_to_node
            neighbors = sorted([(neighbor, G[node][neighbor]['weight']) for neighbor in G.neighbors(node) if neighbor not in visited], key=lambda x: x[1])
            stack.extend(neighbors)
    
    return total_distance

def main(inp_file_paths):
    results = []

    for inp_file_path in inp_file_paths:
        try:
            edges = parse_inp_pipes_section(inp_file_path)
            G = construct_graph(edges)
            total_distance = approximate_min_distance(G)
            file_name_only = os.path.basename(inp_file_path)
            results.append((file_name_only, int(total_distance)))
        except Exception as e:
            print(f"Error processing {inp_file_path}: {e}")
            results.append((os.path.basename(inp_file_path), 'Error'))

    print(f"{'File Name':<20} | {'Approx. Min Total Distance (ft)':>30}")
    print('-' * 53)
    for file_name, distance in results:
        distance_str = str(distance) if isinstance(distance, int) else distance
        print(f"{file_name:<20} | {distance_str:>30}")

if __name__ == "__main__":
    inp_file_paths = [
        "../networks/international_systems/01_apulia.inp",
        "../networks/international_systems/02_balerma.inp",
        "../networks/international_systems/03_fossolo.inp",
        "../networks/international_systems/04_pescara.inp",
        "../networks/international_systems/05_modena.inp",
        "../networks/international_systems/06_zhi_jiang.inp",
        "../networks/international_systems/07_marchi_rural.inp",
    ]
    main(inp_file_paths)