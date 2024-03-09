import random
from robot import Robot

class InspectionStrategy:
    ''' Base class for implementing different inspection algorithms. '''
    def __init__(self, network):
        self.network = network

    def next_move(self, robot, robots, network):
        ''' Determines the next move for a robot. Overridden by subclasses. '''
        pass

class RandomWalkStrategy(InspectionStrategy):
    ''' Robots move randomly but avoid going back unless necessary. '''
    def __init__(self, network):
        super().__init__(network)

    def next_move(self, robot, robots, network):
        neighbors, distances = network.get_neighbors_and_distance(robot.position)
        
        valid_neighbors = [neighbor for neighbor in neighbors if neighbor != robot.position and distances[neighbor] > 0]
        
        forward_moves = [neighbor for neighbor in valid_neighbors if neighbor != robot.last_position]
        
        if forward_moves:
            new_position = random.choice(forward_moves)
        elif robot.last_position in valid_neighbors:
            new_position = robot.last_position
        else:
            return None, 0
        
        distance = distances[new_position]
        return new_position, distance

class MultiRobotManager:
    ''' Manages multiple robots in the simulation. '''
    def __init__(self, number_of_robots, initial_positions):
        ''' Initializes robots based on the given number and their initial positions. '''
        self.robots = [Robot(i, position) for i, position in enumerate(initial_positions)]
