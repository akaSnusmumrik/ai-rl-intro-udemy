import pandas as pd
import  numpy as np
import hashlib

class TicTacToes_Agent:
    def __init__(self, epsilon, symbol, curiosity):
        self.field = pd.DataFrame([[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]
                                   ]
                                  )
        self.value_funct = dict()
        self.episode_states = []
        self.epsilon = epsilon
        self.symbol = symbol
        self.curiosity = curiosity # [0:1], the higher the more curious the algorithm to unseen states


    def conduct_action(self):
        possible_moves = []
        for i in range(self.field.shape[0]):
            for j in range(self.field.shape[1]):
                if self.field.iloc[i, j] == 0:
                    possible_moves.extend([i, j])

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
        self.field[chosen_move[0], chosen_move[1]] = self.symbol
        self.episode_states.extend(
            hashlib.sha256(self.field.values.tobytes()).hexdigest()
            )








