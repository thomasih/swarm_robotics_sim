import pygame
import random
from network import Network
from robot import Robot

class SimulationManager:
    ''' Manages simulation; initialises network and robot '''
    def __init__(self, network_file):
        ''' Simulation manager object constructor '''
        self.network = Network(network_file)
        # Robot starts at first node in the network...
        self.robot = Robot(list(self.network.G.nodes())[0])
        self.setup_pygame()
        self.network.scale_network(self.window_width, self.window_height, 50)

    def setup_pygame(self):
        ''' Sets up pygame window and colors '''
        pygame.init()
        self.window_width, self.window_height = 1200, 800
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.colors = {
            'background': (211, 211, 211),
            'network_line': (0, 0, 128),
            'node': (0, 128, 128),
            'robot': (255, 127, 80),
        }

    def run(self):
        ''' Runs the simulation '''
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill(self.colors['background'])
            self.draw_network()
            self.move_robot()
            pygame.display.flip()
            pygame.time.delay(500)

    def draw_network(self):
        ''' Draws the network and nodes '''
        for edge in self.network.G.edges():
            start_pos = self.network.G.nodes[edge[0]]['pos']
            end_pos = self.network.G.nodes[edge[1]]['pos']
            pygame.draw.line(self.screen, self.colors['network_line'], start_pos, end_pos, 1)
        for node in self.network.G.nodes():
            node_pos = self.network.G.nodes[node]['pos']
            pygame.draw.circle(self.screen, self.colors['node'], node_pos, 2)

    def move_robot(self):
        ''' Moves the robot to a random neighbor '''
        robot_pos = self.network.G.nodes[self.robot.position]['pos']
        pygame.draw.circle(self.screen, self.colors['robot'], robot_pos, 5)
        neighbors, distances = self.network.get_neighbors_and_distance(self.robot.position)
        if neighbors:
            new_position = random.choice(neighbors)
            distance = distances[new_position]
            self.robot.move(new_position, distance)