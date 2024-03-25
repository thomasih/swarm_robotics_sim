import pygame
from network import Network
from inspection_strategy import MultiRobotManager, RandomWalkStrategy, AntColonyOptimisation

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
        self.visited_nodes = set([start_position])

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
        ''' Runs simulation until network has been fully covered. '''
        while len(self.visited_nodes) != len(self.network.G.nodes):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.screen.fill(self.colors['background'])
            self.draw_network()

            for robot in self.multi_robot_manager.robots:
                next_position, distance = self.strategy.next_move(robot, self.multi_robot_manager.robots, self.network)
                robot.move(next_position, distance)
                self.visited_nodes.add(next_position)
                
                if hasattr(self.strategy, 'reinforce_pheromone'):
                    self.strategy.reinforce_pheromone((robot.last_position, next_position))

                robot_pos = self.network.G.nodes[robot.position]['pos']
                pygame.draw.circle(self.screen, self.colors['robot'], robot_pos, 5)

            pygame.display.flip()


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

    def get_number_of_nodes(self):
        ''' Returns number of nodes in the network. '''
        return len(self.network.G.nodes)