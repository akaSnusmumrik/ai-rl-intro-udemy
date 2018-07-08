import numpy as np
import matplotlib.pyplot as plt
import random
#nitter, epsilon, prob_lst_a=[0.5, 0.5],
#                        prob_lst_b=[0.5, 0.5],
#                        prob_lst_c=[0.5, 0.5]
class epsilon_greedy_rl(object):

    def __init__(self, epsilon, win_probs):
        self.means = [0, 0, 0]
        self.epsilon = epsilon
        self.win_prob_lst = win_probs

    def exploreORexploit(self):
        throw_coin = np.random.uniform(0, 1)
        if throw_coin < self.epsilon: #exploite
            return 'explore'
        else:
            return 'exploit'

    def play_machine(self, machine_ind):
        # throw_coin = random.uniform(0, 1)
        # if throw_coin < self.win_prob[machine_ind]:
        #     return 1
        # else:
        #     return 0
        #print(machine_ind)
        #print([1-self.win_prob_lst[machine_ind], self.win_prob_lst[machine_ind]])
        return np.random.choice(a=[0, 1], p=[1-self.win_prob_lst[machine_ind], self.win_prob_lst[machine_ind]])

    def choose_machine_for_exploration(self):
        machine_drop_ind = self.means.index(max(self.means))
        ind_list = [0,1,2]
        ind_list.remove(machine_drop_ind)
        return np.random.choice(ind_list)
        #res = self.play_machine(self, machine_ind)

    def PlayOneRound(self, itter):
            itter+=1
            #choose which machine to play
            decision = self.exploreORexploit()
            if decision == 'exploit':
                #play machhine with a max win probability
                machine_ind = np.argmax(self.means)
            else:
                machine_ind = self.choose_machine_for_exploration()

            res = self.play_machine(machine_ind)
            #reevaluate mean probability
            self.means[machine_ind] = (itter-1)*self.means[machine_ind]/itter + res/itter

    def train_agent(self, nitter):
        self.means = [0, 0, 0]
        #print(self.means)
        #print('initial mean: {}'.format(str(self.means)))
        for itter in range(nitter):
            #print('itteration {}'.format(str(itter)))
            self.PlayOneRound(itter)



