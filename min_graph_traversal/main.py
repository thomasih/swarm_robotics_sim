import networkx as nx
import os

def parse_inp_sections(inp_file_path):
    ''' Parses the [PIPES] and [JUNCTIONS] sections of an INP file to return edge data and node count. '''
    with open(inp_file_path, 'r') as file:
        lines = file.readlines()
    
    pipes_section_found = False
    junctions_section_found = False
    edges = []
    node_count = 0
    for line in lines:
        if line.strip() == "[PIPES]":
            pipes_section_found = True
            junctions_section_found = False
            continue
        elif line.strip() == "[JUNCTIONS]":
            junctions_section_found = True
            pipes_section_found = False
            continue
        
        if pipes_section_found:
            if line.strip() == "" or line.strip().startswith(";"):
                if edges:
                    pipes_section_found = False
                continue
            parts = line.split()
            try:
                head_node, tail_node, length = parts[1], parts[2], float(parts[3])
                edges.append((head_node, tail_node, length))
            except ValueError:
                continue
        elif junctions_section_found:
            if line.strip() == "" or line.strip().startswith(";"):
                if node_count:
                    junctions_section_found = False
                continue
            node_count += 1
    
    return edges, node_count

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

def main():
    directory_path = "../networks/test_space/"
    inp_file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith(".inp")]
    results = []

    for inp_file_path in inp_file_paths:
        try:
            edges, node_count = parse_inp_sections(inp_file_path)
            G = construct_graph(edges)
            total_distance = approximate_min_distance(G)
            file_name_only = os.path.basename(inp_file_path)
            results.append((file_name_only, node_count, int(total_distance)))
        except Exception as e:
            print(f"Error processing {inp_file_path}: {e}")
            results.append((os.path.basename(inp_file_path), 'Error', 'Error'))

    results.sort(key=lambda x: x[1] if isinstance(x[1], int) else float('inf'))

    print('-' * 43)
    print(f"{'File Name':<20} | {'Distance (ft)':<20}")
    print('-' * 43)
    for file_name, _, distance in results:
        distance_str = str(distance) if isinstance(distance, int) else distance
        print(f"{file_name:<20} | {distance_str:<20}")

if __name__ == "__main__":
    main()
