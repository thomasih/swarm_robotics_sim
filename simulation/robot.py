class Robot:
    ''' Represents the state of a robot and its behavior in the network. '''
    def __init__(self, robot_id, position):
        ''' Initializes a new robot with a unique ID and starting position. '''
        self.robot_id = robot_id
        self.position = position
        self.last_position = None
        self.distance_covered = 0.0
        self.visited_nodes = {position}
        self.visited_edges = set()

    def move(self, next_position, distance):
        ''' Updates the robot's position, distance covered, and time elapsed. '''
        self.last_position = self.position
        self.position = next_position
        self.distance_covered += distance
        self.visited_nodes.add(next_position)
        self.visited_edges.add((self.last_position, next_position))
