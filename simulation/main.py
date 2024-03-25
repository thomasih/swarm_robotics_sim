import os
from simulation_manager import SimulationManager
from inspection_strategy import RandomWalkStrategy, AntColonyOptimisation

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
    directory_path = "../networks/test_space/"
    network_files = [file for file in os.listdir(directory_path) if file.endswith(".inp")]
    number_of_robots = 10
    strategies = [RandomWalkStrategy, AntColonyOptimisation]
    results = {}

    for network_file in network_files:
        full_path = os.path.join(directory_path, network_file)
        node_count = SimulationManager(full_path, number_of_robots, RandomWalkStrategy).get_number_of_nodes()
        distances = {}
        for strategy in strategies:
            strategy_name = strategy.__name__
            average_distance = run_simulation(full_path, number_of_robots, strategy)
            distances[strategy_name] = average_distance
        random_walk_distance = distances['RandomWalkStrategy']
        pheromone_distance = distances['AntColonyOptimisation']
        percentage_decrease = ((random_walk_distance - pheromone_distance) / random_walk_distance) * 100
        results[network_file] = {
            'Node Count': node_count,
            'RandomWalkStrategy': random_walk_distance,
            'AntColonyOptimisation': pheromone_distance,
            'Percentage Decrease': percentage_decrease,
        }

    sorted_results = sorted(results.items(), key=lambda x: x[1]['Node Count'])

    print('-' * 88) 
    print(f"{'Network File':<20} | {'No. of Nodes':<12} | {'Random (ft)':<15} | {'ACO (ft)':<15} | {'% Decrease':<15}")
    print('-' * 88) 

    total_percentage_decrease = 0
    for network_file, info in sorted_results:
        print(f"{network_file:<20} | {info['Node Count']:<12} | {int(info['RandomWalkStrategy']):<15} | {int(info['AntColonyOptimisation']):<15} | {info['Percentage Decrease']:<15.2f}")
        total_percentage_decrease += info['Percentage Decrease']
    print('-' * 88) 

    average_percentage_decrease = total_percentage_decrease / len(sorted_results)
    print(f"Average Percentage Decrease: {average_percentage_decrease:.2f}%\n")

if __name__ == "__main__":
    main()