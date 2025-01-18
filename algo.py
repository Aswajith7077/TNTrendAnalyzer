import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math



def project_continuous_time_logistic_model(init_pop=20, time_to_run=1, r=0.4, k=300,
                                           sinusoid=False, sinusoid_k0=100, sinusoid_k1=10, sinusoid_tp=10,
                                           modify_k_values=False, modify_initial_pop=False, modify_tp_value=False,
                                           modify_r_value=False, verbose=True):
    """
    Continuous time logistic growth model, with optional sinusoidal carrying capacity.
    
    Arguments:
    - init_pop: Initial population.
    - time_to_run: Total time to run the simulation.
    - r: Growth rate.
    - k: Carrying capacity.
    - sinusoid: Whether to apply sinusoidal variation to carrying capacity.
    - sinusoid_k0: Base value for carrying capacity in sinusoidal case.
    - sinusoid_k1: Amplitude for sinusoidal variation.
    - sinusoid_tp: Time period for the sinusoidal cycle.
    - modify_k_values, modify_initial_pop, modify_tp_value, modify_r_value: Options to modify these parameters.
    - verbose: Whether to print metadata.
    
    Returns:
    - final_pop: The final population at the end of the simulation.
    """

    results = pd.DataFrame({'x': np.linspace(0, time_to_run, time_to_run * 2)})  # Create time array
    metadata = {}  # Metadata to store additional information
    print('Init POP : ',init_pop)
    print('K : ',k)
    
    for i in range(1, 10):  # Run the model with different parameter sets (e.g., different initial populations)
        pop_history = []
        current_k = k

        # Update growth rate 'r' if needed
        if modify_r_value:
            current_r = i / 10
        else:
            current_r = r

        # Modify initial population if needed
        if modify_initial_pop:
            current_pop = i * 100
        else:
            current_pop = init_pop

        # Modify time period 'tp' if needed
        if modify_tp_value:
            tp = i * 10
        else:
            tp = sinusoid_tp

        # Run the population model over time
        for t in np.linspace(0, time_to_run, time_to_run * 2):
            if sinusoid:  # Apply sinusoidal variation to carrying capacity
                if modify_k_values:
                    k_0 = i * 100
                    k_1 = k_0 - i * 75
                else:
                    k_0 = sinusoid_k0
                    k_1 = sinusoid_k1

                current_k = k_0 + k_1 * math.cos(2 * math.pi * t / tp)
            else:  # Use constant carrying capacity
                if modify_k_values:
                    current_k = i * 100
                else:
                    current_k = k

            # Logistic growth equation
            current_pop = current_pop + current_r * current_pop * (1 - current_pop / current_k)
            # print(current_pop,current_k,tp)

            # Check for invalid population values
            if current_pop < 0 or current_pop == math.inf:
                print("Pop dropped to an invalid number, check params!")

            # Store population history
            pop_history.append(current_pop)

        # At this point, 'current_pop' contains the final population at the last time step
        final_pop = current_pop  # Capture the final population value

        # Store metadata for current run
        set_label = "{}".format(i)
        metadata[set_label] = {
            "modify_pop": modify_initial_pop,
            "modify_k_values": modify_k_values,
            "modify_r": modify_r_value,
            "modify_tp": modify_tp_value,
            "pop": init_pop,
            "r": current_r,
            "k": current_k,
            "k0": sinusoid_k0 + i * 100,
            "k1": sinusoid_k1 + i * 100,
            "tp": tp
        }
        results[set_label] = pop_history  # Store the population history for visualization

    # print(pop_history)
    print(final_pop)

    # matplotlib work to plot the population dynamics over time
    # plt.style.use("seaborn-paper")
    # plt.tight_layout()
    
    # Return final population for the last simulation
    return final_pop