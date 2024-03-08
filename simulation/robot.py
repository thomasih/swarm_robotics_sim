class Robot:
    ''' Represents the state of a robot and its behavior in the network. '''
    def __init__(self, robot_id, position):
        ''' Initializes a new robot with a unique ID and starting position. '''
        self.robot_id = robot_id
        self.position = position
        self.last_position = None
        self.distance_covered = 0.0
        self.time_elapsed = 0
        self.path_taken = [position]
        self.active = True

    def move(self, next_position, distance):
        ''' Updates the robot's position, distance covered, and time elapsed. '''
        self.last_position = self.position
        self.position = next_position
        self.distance_covered += distance
        self.time_elapsed += 1
        self.path_taken.append(next_position)

    def get_status(self):
        ''' Returns the current status of the robot. '''
        return {
            'robot_id': self.robot_id,
            'position': self.position,
            'distance_covered': self.distance_covered,
            'time_elapsed': self.time_elapsed,
            'path_taken': self.path_taken,
        }

    def deactivate(self):
        '''Marks the robot as inactive.'''
        self.active = False
