from simulation_manager import SimulationManager

def main():
    '''Opens network file, instantiates simulation with multiple robots, and starts the simulation.'''
    network_file = '../networks/wntr_examples/Net3.inp'
    number_of_robots = 10
    simulation = SimulationManager(network_file, number_of_robots)
    simulation.run()
    print('------------------------------------------')
    print('Simulation finished.')

    total_distance_covered = sum(robot.distance_covered for robot in simulation.multi_robot_manager.robots)
    print(f'Total distance covered by all robots: {round(total_distance_covered, 2)} feet')

    total_nodes = len(simulation.network.G.nodes())
    visited_nodes = len(simulation.visited_nodes)
    coverage_percentage = (visited_nodes / total_nodes) * 100
    print(f'Network Coverage: {coverage_percentage:.2f}%')
    print('------------------------------------------')

if __name__ == "__main__":
    main()
