import numpy as np
import matplotlib.pyplot as plt
import random
#nitter, epsilon, prob_lst_a=[0.5, 0.5],
#                        prob_lst_b=[0.5, 0.5],
#                        prob_lst_c=[0.5, 0.5]
class epsilon_greedy_rl(object):

    def __init__(self, win_probs):
        self.means = [10, 10, 10]
        self.win_prob_lst = win_probs

    def play_machine(self, machine_ind):
        return np.random.choice(a=[0, 1], p=[1-self.win_prob_lst[machine_ind], self.win_prob_lst[machine_ind]])

    def choose_machine_for_exploration(self):
        machine_drop_ind = self.means.index(max(self.means))
        ind_list = [0,1,2]
        ind_list.remove(machine_drop_ind)
        return np.random.choice(ind_list)
        #res = self.play_machine(self, machine_ind)

    def PlayOneRound(self, itter):
            itter+=2
            #play machhine with a max win probability
            machine_ind = np.argmax(self.means)
            res = self.play_machine(machine_ind)
            #reevaluate mean probability
            self.means[machine_ind] = (itter-1)*self.means[machine_ind]/itter + res/itter

    def train_agent(self, nitter):
        res = pd.DataFrame([self.means])
        #print(self.means)
        #print('initial mean: {}'.format(str(self.means)))
        for itter in range(nitter):
            #print('itteration {}'.format(str(itter)))
            self.PlayOneRound(itter)
            res=res.append([self.means], ignore_index=True)
        #res=pd.DataFrame(res)
        res.plot()
        plt.show()
        return res

import matplotlib.pyplot as plt
import pandas as pd

agent = epsilon_greedy_rl([0.1, 0.3, 0.6])
print(agent.train_agent(20000))