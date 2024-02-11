# –––––––––– Robot moves along directed graph in random path –––––––––

import pygame
import wntr
import random

wn = wntr.network.WaterNetworkModel('../networks/wntr_examples/Net3.inp')
G = wn.to_graph()

# bounds of graph
min_x = min([G.nodes[node]['pos'][0] for node in G.nodes])
min_y = min([G.nodes[node]['pos'][1] for node in G.nodes])
max_x = max([G.nodes[node]['pos'][0] for node in G.nodes])
max_y = max([G.nodes[node]['pos'][1] for node in G.nodes])

# window dimensions and margin
window_width, window_height = 1200, 800
margin = 50

# scale and offset calculation with margin
scale_x = (window_width - 2 * margin) / (max_x - min_x)
scale_y = (window_height - 2 * margin) / (max_y - min_y)
offset_x = -min_x * scale_x + margin
offset_y = -min_y * scale_y + margin

# apply scale and offset with margin
for node in G.nodes:
    pos = G.nodes[node]['pos']
    scaled_pos = (int(pos[0] * scale_x + offset_x), int(pos[1] * scale_y + offset_y))
    G.nodes[node]['pos'] = scaled_pos

# init pygame and define colours
pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
BACKGROUND_COLOR = (211, 211, 211) 
NETWORK_LINE_COLOR = (0, 0, 128)
NODE_COLOR = (0, 128, 128)
ROBOT_COLOR = (255, 127, 80)

# robot starts at first node
robot_position = list(G.nodes())[0]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    # draw network
    for edge in G.edges():
        start_pos = G.nodes[edge[0]]['pos']
        end_pos = G.nodes[edge[1]]['pos']
        pygame.draw.line(screen, NETWORK_LINE_COLOR, start_pos, end_pos, 1)

    # draw nodes as small black dots
    for node in G.nodes():
        node_pos = G.nodes[node]['pos']
        pygame.draw.circle(screen, NODE_COLOR, node_pos, 2)

    # draw the robot
    robot_pos = G.nodes[robot_position]['pos']
    pygame.draw.circle(screen, ROBOT_COLOR, robot_pos, 5)

    # update the robot's position
    next_nodes = list(G.neighbors(robot_position))
    random.shuffle(next_nodes)
    robot_position = random.choice(next_nodes) if next_nodes else robot_position

    pygame.display.flip()
    pygame.time.delay(1000)

pygame.quit()
