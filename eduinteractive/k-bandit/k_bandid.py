#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt

class Env:
    def __init__(self, k):
        self.centers = np.random.normal(10.0, 5.0, k)
        self.sigmas = np.full((10,1), 0.1)#np.abs(np.random.normal(5.0, 2.0, k))

    def action(self, idx):
        return np.random.normal(self.centers[idx], self.sigmas[idx])

    def get_best_action_idx(self):
        return np.argmax(self.centers)

    def __str__(self):
        return ("Best action index: %s\ndistribution centers: %s"
                % (str(self.get_best_action_idx()), str(self.centers)))


# Simple agent for k-armed problem
class Agent:

    # @k the number of bandits
    def __init__(self, k):
        self.k = k
        self.action_value_est = np.zeros(shape=(k, 1))
        self.action_value_cases = np.zeros(shape=(k, 1))

    # @env the target environment to run in
    # @steps_count how many steps to make
    # @params the dict of agent extra params
    def run_agent(self, env, steps_count, params):
        history = []
        total_reward = 0.0

        for i in range(steps_count):
            tactics_selector = np.random.random()

            if tactics_selector < params["epsilon"]:
                # exploration branch with epsilon probability
                action_idx = np.random.randint(0, self.k)
            else:
                # exploitation branch (greedy branch) else
                action_idx = np.argmax(self.action_value_est, 0)

                if len(action_idx) > 1:
                    action_idx = np.random.random_integers(0, len(action_idx) - 1)
                else:
                    action_idx = action_idx[0]

            reward = env.action(action_idx)

            history.append(action_idx)
            total_reward += reward

            # update the estimated reward
            Q_i = self.action_value_est[action_idx, 0]   # (R1 + R2 + .. + RN)/N
            N_i = self.action_value_cases[action_idx, 0]   # N
            Q_next = (Q_i * float(N_i) + reward) / (N_i + 1.0)

            self.action_value_est[action_idx, 0] = Q_next
            self.action_value_cases[action_idx, 0] += 1

        return (history, total_reward)

    # @crowd_size number of agents to use
    def run_crowd(self, env, steps_count, params, crowd_size):
        for i in range(crowd_size):
            self.run_agent(env, steps_count, params)


def run_single_experiment():
    current_env = Env(10)

    a = Agent(10)
    history, cummulative_reward = a.run_agent(current_env, 1000, {'epsilon' : 0.1})

    best_action_idx = current_env.get_best_action_idx()

    optimal_action_selected = (history == best_action_idx)

    plt.plot(optimal_action_selected)
    plt.show()

def run_experiment_series():
    experiments_count = 1000
    epsilon_variants = [0.0, 0.05, 0.1, 0.15, 0.2]

    optimal_action_selected = np.zeros(1000)

    for epsilon in epsilon_variants:
        for i in range(experiments_count):
            current_env = Env(10)

            a = Agent(10)
            history, cummulative_reward = a.run_agent(current_env, 1000, {'epsilon' : epsilon})

            best_action_idx = current_env.get_best_action_idx()

            print("Current env: ", current_env)

            optimal_action_selected += (history == best_action_idx)

        optimal_action_selected = optimal_action_selected / experiments_count

        plt.plot(optimal_action_selected)
    plt.legend(['Epsilon: %f' % epsilon for epsilon in epsilon_variants])

    plt.xlabel('Step #')
    plt.ylabel('Part of best action selected')

    plt.show()

run_experiment_series()
