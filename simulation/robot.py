class Robot:
    ''' State of robot and its behaviour '''
    def __init__(self, position):
        ''' Robot object constructor '''
        self.position = position
        self.distance_covered = 0.0
        self.time_elapsed = 0

    def move(self, next_position, distance):
        '''Moves robots position and updates metrics '''
        self.position = next_position
        self.distance_covered += distance
        self.time_elapsed += 1

    def get_status(self):
        ''' Returns robot status '''
        return {
            'position': self.position,
            'distance_covered': self.distance_covered,
            'time_elapsed': self.time_elapsed,
        }