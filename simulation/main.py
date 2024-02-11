from simulation_manager import SimulationManager

def main():
    ''' Opens network file and instantiates simulation '''
    network_file = '../networks/wntr_examples/Net3.inp'
    simulation = SimulationManager(network_file)
    simulation.run()
    print('------------------------------------------');
    print('Simulation finished.');
    print('Distance covered:', round(simulation.robot.distance_covered,2), 'feet');
    print('Time elapsed:', simulation.robot.time_elapsed, 'steps');
    print('------------------------------------------');

if __name__ == "__main__":
    main()