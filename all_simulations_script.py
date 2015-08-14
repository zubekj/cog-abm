import os


networks = {"max_avg_bet", "max_avg_clust", "max_max_bet", "max_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "min_max_clos"}


# simulations
for i in xrange(20):
    
    for network in networks:
        os.system("python steels_main.py -s /examples/simulations/shift_simulations/simulation_"+network+"_to_clique.json -r  /results_of_simulation/shift_sim_results/results_"+network+"_to_clique"+format(i))
    
    os.system("python steels_main.py -s /examples/simulations/shift_simulations/simulation_line_to_clique.json -r  /results_of_simulation/shift_sim_results/results_line_to_clique"+format(i))
    os.system("python steels_main.py -s /examples/simulations/shift_simulations/simulation_hub_to_clique.json -r  /results_of_simulation/shift_sim_results/results_hub_to_clique"+format(i))
    os.system("python steels_main.py -s /examples/simulations/shift_simulations/simulation_ring_to_clique.json -r  /results_of_simulation/shift_sim_results/results_ring_to_clique"+format(i))


# analyzer
results = {"CSA", "DSA", "CLA", "DG_CLA"}
for result in results:
    for i in xrange(20):
        for network in networks:




# pandas