def steels_experiment_continuation(simulation, old_params, new_params):

    # Changing parameters to suit whole new simulation.
    old_params["num_iter"] += new_params["num_iter"]

    old_iteration = simulation.get_iteration_counter()
    for network in new_params["networks"]:
        network["start"] += old_iteration - 1
        old_params["networks"].append(network)

    simulation.set_networks(old_params["networks"])

    results = simulation.continue_(new_params["new_iter"], old_params["dump_freq"])

    return results, simulation, old_params
