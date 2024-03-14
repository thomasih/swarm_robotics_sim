import random
from robot import Robot
import math

class InspectionStrategy:
    ''' Base class for implementing different inspection algorithms. '''
    def __init__(self, network):
        ''' Base constructor of inspection strategy class. '''
        self.network = network

    def next_move(self, robot, robots, network):
        ''' Determines the next move for a robot. Overridden by subclasses. '''
        pass

class RandomWalkStrategy(InspectionStrategy):
    ''' Robots move randomly but avoid going back unless necessary. '''
    def __init__(self, network):
        ''' Calls constructor of base class. '''
        super().__init__(network)

    def next_move(self, robot, robots, network):
        ''' Makes random choice for robots next move. '''
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

class PheromoneStrategy(InspectionStrategy):
    ''' Strategy based on ant colony optimisation (ACO) algorithm. '''
    def __init__(self, network):
        ''' Calls constructor of base class and intialises class variables. '''
        super().__init__(network)
        self.pheromones = {}
        for edge in network.G.edges():
            self.pheromones[(edge[0], edge[1])] = 0.1
            self.pheromones[(edge[1], edge[0])] = 0.1
        self.robot_knowledge = {}

    def reinforce_pheromone(self, edge, amount=0.1):
        ''' Reinforces edge if it exists in both directions. '''
        if edge in self.pheromones:
            self.pheromones[edge] += amount
        reverse_edge = (edge[1], edge[0])
        if reverse_edge in self.pheromones:
            self.pheromones[reverse_edge] += amount

    def update_robot_knowledge(self, robot_id, last_position, visited_nodes, visited_edges):
        ''' Shares visited nodes and edges with all robots in communciation range. '''
        for other_id, (other_last_position, nodes, edges) in self.robot_knowledge.items():
            if other_id != robot_id and self.can_communicate(last_position, other_last_position):
                visited_nodes |= nodes
                visited_edges |= edges
        
        self.robot_knowledge[robot_id] = (last_position, visited_nodes, visited_edges)

    def can_communicate(self, robot_id1, robot_id2):
        ''' Calculates whether two robots are within communication range. '''
        position1 = self.network.G.nodes[robot_id1]['pos']
        position2 = self.network.G.nodes[robot_id2]['pos']

        distance = math.sqrt((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2)

        # Distance must be less than given value (in ft) to communicate
        return distance <= 100

    def next_move(self, robot, robots, network):
        ''' Moves robot, prioritising unvisited nodes, then lowest pheromone path. '''
        self.update_robot_knowledge(robot.robot_id, robot.position, robot.visited_nodes, robot.visited_edges)
        neighbors, distances = network.get_neighbors_and_distance(robot.position)

        unvisited_neighbors = [(neighbor, distances[neighbor]) for neighbor in neighbors if neighbor not in robot.visited_nodes]
        
        if unvisited_neighbors:
            next_position = min(unvisited_neighbors, key=lambda x: self.pheromones.get((robot.position, x[0]), 0))[0]
            distance = distances[next_position]
            return next_position, distance
        else:
            valid_moves = [(neighbor, distances[neighbor]) for neighbor in neighbors]
            next_position = min(valid_moves, key=lambda x: self.pheromones.get((robot.position, x[0]), float('inf')))[0]
            distance = distances[next_position]
            return next_position, distance

class MultiRobotManager:
    ''' Manages multiple robots in the simulation. '''
    def __init__(self, number_of_robots, initial_positions):
        ''' Initializes robots based on the given number and their initial positions. '''
        self.robots = [Robot(i, position) for i, position in enumerate(initial_positions)]