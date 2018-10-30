import pandas as pd
import  numpy as np
import hashlib

class TicTacToes_Agent:
    def __init__(self, epsilon, alpha, symbol, curiosity):
        self.field = pd.DataFrame([[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]
                                   ]
                                  )
        self.value_funct = dict()
        self.episode_states = []
        self.epsilon = epsilon #exploration/exploitation
        self.symbol = symbol
        self.curiosity = curiosity # default value function, [0:1], the higher the more curious the algorithm to unseen state
        self.alpha = alpha #learning rate for value function

    def chose_conduct_action(self):
        possible_moves = []
        for i in range(self.field.shape[0]):
            for j in range(self.field.shape[1]):
                if self.field.iloc[i, j] == 0:
                    possible_moves.append([i, j])

        if np.random.choice(10)/10<self.epsilon: #explore
            #pick a random move
            ind = np.random.choice(len(possible_moves), 1)[0]
            chosen_move = possible_moves[ind]
        else:
            max_V = 0
            chosen_move = possible_moves[0]
            for move in possible_moves:
                cur_val = self.field[move[0], move[1]]
                self.field[move[0], move[1]] = self.symbol
                state_key = hashlib.sha256(self.field.values.tobytes()).hexdigest()
                V = self.value_funct.get(state_key, self.curiosity)
                if V > max_V:
                    max_V = V
                    chosen_move = move
                    self.field[move[0], move[1]] = cur_val

        #conduct choosen action:
        self.field.iloc[chosen_move[0], chosen_move[1]] = self.symbol
        self.episode_states.append(
            hashlib.sha256(self.field.values.tobytes()).hexdigest()
            )


    def update_value_function(self, winer):
        if winer == self.symbol:
            result = 1
        if winer == 0.5:
            result = 0.5
        else:
            result = -1

        self.value_funct[self.episode_states[-1]] = result #set value function to the last state
        previous_state = self.episode_states[-1]
        for state_key in reversed(self.episode_states[:-1]):
            self.value_funct[state_key] = self.value_funct.get(state_key, self.curiosity) + self.epsilon()*(self.value_funct[previous_state] -
                                                                                self.value_funct.get(state_key, self.curiosity))
            previous_state = state_key

class Play:
    def __init__(self, epsilon, alpha, curiosity, train_episodes):
        self.field = pd.DataFrame([[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]
                                   ]
                                  )
        self.agend1 = TicTacToes_Agent(epsilon, alpha, 1, curiosity)
        self.agend2 = TicTacToes_Agent(epsilon, alpha, -1, curiosity)
        self.train_episodes = train_episodes
        self.winer = np.nan

    def gameover_check(self):
        if ((self.field.sum(axis=1)==3).any())|(
                (self.field.sum(axis=0) == 3).any())|(
                sum([self.field.iloc[i, self.field.shape[0] - i - 1] for i in range(self.field.shape[0])]) == 3)|(
                sum([self.field.iloc[i, i] for i in range(self.field.shape[0])]) == 3):
            self.winer = 1

        if ((self.field.sum(axis=1) == -3).any())|(
                (self.field.sum(axis=0) == -3).any())|(
                sum([self.field.iloc[i, self.field.shape[0] - i - 1] for i in range(self.field.shape[0])]) == -3)|(
                sum([self.field.iloc[i, i] for i in range(self.field.shape[0])]) == -3):
            self.winer = -1

        if (self.field == 0).any().any():
            self.winer=0.5




    def train(self):
        # training
        for i in range(self.train_episodes):
            print("Episode {}".format(i))
            while np.isnan(self.winer):
                self.agend1.chose_conduct_action()
                self.agend2.field = self.agend1.field
                self.gameover_check()
                if np.isnan(self.winer)==False:
                    break

                self.agend2.chose_conduct_action()
                self.agend1.field = self.agend2.field
                self.gameover_check()
                if np.isnan(self.winer)==False:
                    break

            self.agend1.update_value_function(self.winer)
            self.agend2.update_value_function(self.winer)





game = Play(0.7, 1, 0.6, 100)
game.train()