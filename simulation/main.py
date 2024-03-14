from simulation_manager import SimulationManager
from inspection_strategy import RandomWalkStrategy, PheromoneStrategy

def run_simulation(network_file, number_of_robots, strategy_class):
    ''' Runs simulation specified amount of times and returns average total distance. '''
    total_distance = 0
    for _ in range(5):
        simulation = SimulationManager(network_file, number_of_robots, strategy_class)
        simulation.run()
        distance_covered = sum(robot.distance_covered for robot in simulation.multi_robot_manager.robots)
        total_distance += distance_covered
    average_distance = total_distance / 5
    return average_distance

def main():
    ''' Defines metrics and runs simulation, plotting results in a table. '''
    network_files = [
        "01_apulia.inp",
        "02_balerma.inp",
        "03_fossolo.inp",
        "04_pescara.inp",
        "05_modena.inp",
        "06_zhi_jiang.inp",
        "07_marchi_rural.inp"
    ]
    number_of_robots = 10
    strategies = [RandomWalkStrategy, PheromoneStrategy]
    results = {}

    for network_file in network_files:
        node_count = SimulationManager(f'../networks/international_systems/{network_file}', number_of_robots, RandomWalkStrategy).get_number_of_nodes()
        distances = {}
        for strategy in strategies:
            strategy_name = strategy.__name__
            average_distance = run_simulation(f'../networks/international_systems/{network_file}', number_of_robots, strategy)
            distances[strategy_name] = average_distance
        random_walk_distance = distances['RandomWalkStrategy']
        pheromone_distance = distances['PheromoneStrategy']
        percentage_decrease = ((random_walk_distance - pheromone_distance) / random_walk_distance) * 100
        results[network_file] = {
            'Node Count': node_count,
            'RandomWalkStrategy': random_walk_distance,
            'PheromoneStrategy': pheromone_distance,
            'Percentage Decrease': percentage_decrease,
        }

    print(f"{'Network File':<20} | {'Nodes':<6} | {'RandomWalk':<12} | {'Pheromone':<12} | {'% Decrease':<12}")
    print('-' * 74)
    for network_file, info in results.items():
        print(f"{network_file:<20} | {info['Node Count']:<6} | {info['RandomWalkStrategy']:<12.2f} | {info['PheromoneStrategy']:<12.2f} | {info['Percentage Decrease']:<12.2f}")

if __name__ == "__main__":
    main()