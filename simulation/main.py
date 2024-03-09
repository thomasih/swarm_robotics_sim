from simulation_manager import SimulationManager

def main():
    '''Opens network file, instantiates simulation with multiple robots, and starts the simulation.'''
    network_file = '../networks/international_systems/05_modena.inp'
    number_of_robots = 10
    simulation = SimulationManager(network_file, number_of_robots)
    simulation.run()
    print('------------------------------------------')
    print('Simulation finished.')
    total_distance_covered = sum(robot.distance_covered for robot in simulation.multi_robot_manager.robots)
    print(f'Total distance covered by all robots: {round(total_distance_covered, 2)} feet')
    print('------------------------------------------')

if __name__ == "__main__":
    main()
