#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt

class Env:
    def __init__(self, k):
        self.centers = np.random.normal(10.0, 5.0, k)
        self.sigmas = np.abs(np.random.normal(5.0, 2.0, k))

    def action(self, idx):
        return np.random.normal(self.centers[idx], self.sigmas[idx])

    def get_best_action_idx(self):
        return np.argmax(self.centers)

    def __str__(self):
        return ("Best action index: %s\ndistribution centers: %s"
                % (str(self.get_best_action_idx()), str(self.centers)))

class NonStationaryEnv:
    def __init__(self, k, stationary=False):
        self.k = k
        self.centers = np.random.normal(10.0, 5.0, k)
        self.sigmas = np.abs(np.random.normal(5.0, 2.0, k))
        # abs center shift per 100 actions
        if stationary:
            self.migration = np.zeros(shape=(k,))
        else:
            self.migration = np.random.normal(3.0, 3.0, k)
        self.time = 0.0;

    def get_current_center(self, idx):
        return self.centers[idx] + self.migration[idx] * self.time / 100.0

    def action(self, idx):
        # non-stationary task: the action result slowly migrates with time
        value = np.random.normal(self.get_current_center(idx), self.sigmas[idx])
        self.time += 1.0
        return value

    # returns a matrix-string of best index values over the history
    # @steps the number of steps for the
    #
    # RETURNS: (steps,) shaped array of best action indexes vs time step
    def get_best_action_idx(self, steps=1000):
        best_idx = np.zeros(shape=(steps,))
        for t in range(steps):
            self.time = float(t)
            max_idx = 0
            max_val = self.get_current_center(max_idx)
            for i in range(self.k):
                val = self.get_current_center(i)
                if (val > max_val):
                    max_val = val
                    max_idx = i
            best_idx[t] = max_idx

        return best_idx

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
    current_env = NonStationaryEnv(10)

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
            current_env = NonStationaryEnv(10)

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

    plt.title('Non-stationary k-bandid problem, 10 actions, normal '
              'reward distribution, normal distribution shift with time')

    plt.show()

run_experiment_series()
