import numpy as np
import pandas as pd
import scripts.task_utils as task_utils

class Scenario:
    def __init__(self, scenario_creator, skip_simulation=False):
        self.scenario_creator = scenario_creator

        prompt = """Determine the mass of the most massive star."""
        final_answer_units = "kg"

        self.binary_sim = self.scenario_creator.create_binary(prompt, final_answer_units, skip_simulation=skip_simulation)

    def true_answer(self, N_obs=None, verification=True, return_empirical=False) -> float:
        """
        Return the true answer for the environment.
        
        Args:
            N_obs: Number of observations to use (if None, use all)
            verification: Whether to verify values match
            return_empirical: If True, return the empirically derived value;
                            if False, return the value inputted into the simulation or using Rebound simulated details typically hidden
        """
        # Load simulation data
        df = pd.read_csv(f"scenarios/detailed_sims/{self.binary_sim.filename}.csv")
        
        if N_obs is not None:
            indices = np.linspace(0, len(df) - 1, N_obs)
            df = df.iloc[indices].reset_index(drop=True)

        # Calculate masses using task_utils
        M1, M2 = task_utils.star_masses(df, self.binary_sim, verification=verification, return_empirical=return_empirical)
        
        # Return the larger mass
        largest_mass = max(M1, M2)

        if verification:
            assert abs(largest_mass - max(self.binary_sim.star1_mass, self.binary_sim.star2_mass)) < 0.02 * max(self.binary_sim.star1_mass, self.binary_sim.star2_mass), \
                   f"{largest_mass} and {max(self.binary_sim.star1_mass, self.binary_sim.star2_mass)} are not within 2% of each other"

        if return_empirical:
            return largest_mass
        else:
            return max(self.binary_sim.star1_mass, self.binary_sim.star2_mass)
