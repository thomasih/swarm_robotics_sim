import pygame
import random
from network import Network
from robot import Robot
from inspection_strategy import RandomWalkStrategy, MultiRobotManager

class SimulationManager:
    ''' Manages the simulation; initializes the network, robots, and inspection strategy. '''
    def __init__(self, network_file, number_of_robots=1, strategy=RandomWalkStrategy):
        ''' Simulation manager object constructor. '''
        self.network = Network(network_file)
        start_position = list(self.network.G.nodes())[0]
        initial_positions = [start_position for _ in range(number_of_robots)]
        self.multi_robot_manager = MultiRobotManager(number_of_robots, initial_positions)
        self.strategy = strategy(self.network)
        self.setup_pygame()
        self.network.scale_network(self.window_width, self.window_height, 50)
        self.all_robots_stopped = False
        self.visited_nodes = set()

    def setup_pygame(self):
        ''' Sets up the pygame window and colors. '''
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
        ''' Runs the simulation, updating the display and robot positions. '''
        count = 0
        while count < 40:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.screen.fill(self.colors['background'])
            self.draw_network()
            all_inactive = self.move_robots()
            pygame.display.flip()
            pygame.time.delay(200)
            count += 1
            if all_inactive:
                break

    def draw_network(self):
        ''' Draws the water distribution network and nodes on the screen. '''
        for edge in self.network.G.edges():
            start_pos = self.network.G.nodes[edge[0]]['pos']
            end_pos = self.network.G.nodes[edge[1]]['pos']
            pygame.draw.line(self.screen, self.colors['network_line'], start_pos, end_pos, 1)
        for node in self.network.G.nodes():
            node_pos = self.network.G.nodes[node]['pos']
            pygame.draw.circle(self.screen, self.colors['node'], node_pos, 2)

    def move_robots(self):
        ''' Moves each robot based on the selected inspection strategy (if they are still active) and draws them. '''
        all_inactive = 1
        for robot in self.multi_robot_manager.robots:
            if robot.active:
                new_position, distance = self.strategy.next_move(robot, self.multi_robot_manager.robots, self.network)
                if new_position is not None:
                    all_inactive = 0
                    robot.move(new_position, distance)
                    self.visited_nodes.add(new_position)
                else:
                    robot.deactivate()

            robot_pos = self.network.G.nodes[robot.position]['pos']
            pygame.draw.circle(self.screen, self.colors['robot'], robot_pos, 5)
        return all_inactive
