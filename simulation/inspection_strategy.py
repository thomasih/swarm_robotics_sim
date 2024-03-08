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
    ''' A simple inspection strategy where robots move randomly, excluding invalid moves. '''
    def __init__(self, network):
        super().__init__(network)

    def next_move(self, robot, robots, network):
        neighbors, distances = network.get_neighbors_and_distance(robot.position)
        
        # Exclude the last position and positions that would result in a move of distance 0
        valid_neighbors = [neighbor for neighbor in neighbors if neighbor != robot.position and distances[neighbor] > 0]
        
        # Further exclude the robot's last position to prevent moving back
        if robot.last_position is not None and robot.last_position in valid_neighbors:
            valid_neighbors.remove(robot.last_position)
        
        if valid_neighbors:
            new_position = random.choice(valid_neighbors)
            distance = distances[new_position]
            return new_position, distance
        return None, 0



class MultiRobotManager:
    ''' Manages multiple robots in the simulation. '''
    def __init__(self, number_of_robots, initial_positions):
        ''' Initializes robots based on the given number and their initial positions. '''
        self.robots = [Robot(i, position) for i, position in enumerate(initial_positions)]
