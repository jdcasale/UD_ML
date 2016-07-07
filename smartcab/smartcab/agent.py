import random

#import matplotlib.pyplot as plt
from collections import defaultdict
from collections import OrderedDict
from environment import Agent
from environment import Environment
from planner import RoutePlanner
from simulator import Simulator

ACTIONS = [
    None,
    'right',
    'left',
    'forward',
]

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""
    def __init__(self, env, gamma):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        #lookup table for values of our Q-function
        self.qtable = defaultdict(float)
        #lookup table for state transition probabilities
        self.ptable = defaultdict(float)
        self.r_table = defaultdict(float)
        self.num_actions_taken = 1.0
        self.LEARNING_RATE = 1.0/self.num_actions_taken
        self.net_trip_reward = 0
        self.GAMMA = gamma
        self.NUM_PENALTIES_INCURRED = 0
    def get_penalties_incurred(self):
        return self.NUM_PENALTIES_INCURRED
    def get_actions_taken(self):
        return self.num_actions_taken
    def get_average_reward_per_action(self):
        return float(self.net_trip_reward)/float(self.num_actions_taken)
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
    def get_state(self):
        self.LEARNING_RATE = 1#max(10.0/(10 + self.num_actions_taken), .1)
        inputs = self.env.sense(self)
        inputs['next_waypoint'] = self.next_waypoint
        return ','.join(map(lambda x: x[1] or 'None', inputs.items()))

    def update_reward_for_state(self, state, reward):
        # might want to modify this not to bias toward first reward seen
        self.r_table[state] = self.r_table.get(state) \
                              + self.LEARNING_RATE \
                                * (reward-self.r_table.get(state)) \
            if self.r_table.has_key(state) else reward
    def policy(self, state):
        # Implement GLIE by choosing the action
        # prescribed by our policy only with a certain percentage
        # of cases, starting at 100 and decaying with each action taken
        # bottoming out at choosing a random action 6% of the time
        if max(50-self.num_actions_taken, 3) < random.randint(1,50):
            action_expected_value_pairs = [(a, self.qtable.get((state, a))) for a in ACTIONS]
            return max(action_expected_value_pairs, key=lambda x: x[1])[0]
        else:
            return random.choice(ACTIONS)
    def Q(self, state, action, value=None):
        if value:
            self.qtable[(state, action)] = value
        else:
            return self.qtable.get((state, action), 0)

    def update(self, t):
        # TODO: Update state
        self.num_actions_taken += 1
        _ = self.env.sense(self)
        _ = self.env.get_deadline(self)
        # from route planner, also displayed by simulator
        self.next_waypoint = self.planner.next_waypoint()

        starting_state = self.get_state()

        # TODO: Select action according to your policy
        action = self.policy(starting_state)
        # Execute action and get reward
        reward = self.env.act(self, action)
        if reward < 0:
            self.NUM_PENALTIES_INCURRED += 1
        self.net_trip_reward += reward
        #print "Net reward: {}".format(self.net_trip_reward)
        new_state = self.get_state()
        self.update_reward_for_state(new_state, reward)
        # TODO: Learn policy based on state, action, reward
        self.q_function(starting_state, action, new_state, reward)



    def q_function(self, s, a, s_prime, reward):
        old_qsa = self.Q(s, a)
        print self.GAMMA
        # Ugly math-to-code -- for an easier-to-read version, see http://artint.info/html/ArtInt_265.html
        new_qsa = \
            (1-self.LEARNING_RATE)* old_qsa\
            + self.LEARNING_RATE * (reward +
            self.GAMMA * max(map(lambda x : self.Q(*x), [(s_prime, a_prime) for a_prime in ACTIONS])))
        self.Q(s,a, new_qsa)


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    gammas = [x/10. for x in xrange(0,10)]
    gamma_to_success_rate = OrderedDict()
    gamma_to_average_reward = OrderedDict()
    # Run a simulation for each sample gamma value to test which
    # choice of gamma results in the most successful agent
    for gamma in gammas:
        # Run 10 trials over each choice of gamma to get average performance metrics
        for trial in xrange(10):
            e = Environment()  # create environment (also adds some dummy traffic)
            a = e.create_agent(LearningAgent, (gamma))  # create agent
            e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

            # Now simulate it
            sim = Simulator(e, update_delay=.0)  # reduce update_delay to speed up simulation
            sim.run(n_trials=50)  # press Esc or close pygame window to quit

            gamma_to_success_rate[a.GAMMA] = gamma_to_success_rate.get(a.GAMMA, 0) + sim.env.successful_trials
            gamma_to_average_reward[a.GAMMA] = gamma_to_average_reward.get(a.GAMMA,0) + a.get_average_reward_per_action()

        # Get the average of the 10 trials
    for gamma in gamma_to_average_reward.keys():
        gamma_to_average_reward[gamma] = gamma_to_average_reward[gamma]/10
        gamma_to_success_rate[gamma] = gamma_to_success_rate[gamma]/10
    print gamma_to_average_reward
    print gamma_to_success_rate


if __name__ == '__main__':
    run()