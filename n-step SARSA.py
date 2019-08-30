# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 10:31:05 2019
@author: BassemJ
"""

import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

BOARD_ROWS = 7
BOARD_COLS = 10
WIN_STATE = (3, 7)
START = (3, 0)
WIND = [0,0,0,1,1,1,2,2,1,0]

class State:
    def __init__(self, state=START):
        self.state = state
        self.actions = ["up", "down", "left", "right"]
        self.isEnd = False

    def giveReward(self):
        if self.state == WIN_STATE:
            return 1
        else:
            return -1        

    def isEndFunc(self):
        if (self.state == WIN_STATE):
            self.isEnd = True

    def nxtPosition(self, action):        
#        action: up, down, left, right
#        -------------
#        0 | 1 | 2| 3| 4| 5| 6| 7| 8| 9|
#        1 |
#        2 |
#        3 |
#        4 |
#        5 |
#        6 |  
        if action == "up":
            nxtState = (min(max(self.state[0] - (1 + WIND[self.state[1]]),0),6), self.state[1])
        elif action == "down":
            nxtState = (min(max(self.state[0] + 1 - WIND[self.state[1]],0),6), self.state[1])
        elif action == "left":
            nxtState = (max(self.state[0] - WIND[self.state[1]],0), max(self.state[1] - 1,0))
        else:
            nxtState = (max(self.state[0] - WIND[self.state[1]],0), min(self.state[1] + 1,9))
        return nxtState


class Agent:

    def __init__(self):
        self.states = [START]
        self.rewards = []
        self.path = []
        self.pathslength = []
        self.State = State()
        self.epsilon = 0.01
        self.alpha = 0.4
        self.gamma = 0.99
        self.bootstrap = 4
        self.q = {}

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)

    def learnQ(self, state, action, G):
        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = G 
        else:
            self.q[(state, action)] = self.q[(state, action)] + self.alpha * (G - self.q[(state, action)])

    def chooseAction(self, state):
        if np.random.uniform(0, 1) <= self.epsilon:
            action = np.random.choice(self.State.actions)
        else:
            q = [self.getQ(state, a) for a in self.State.actions]
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self.State.actions)) if q[i] == maxQ]
                i = np.random.choice(best)
            else:
                i = q.index(maxQ)

            action = self.State.actions[i]
        return action

    def takeAction(self, action):
        position = self.State.nxtPosition(action)
        return State(state=position)

    def reset(self):
        self.states = [START]
        self.rewards = []
        self.path = []
        self.State = State()

    def play(self, rounds=10):
        i = 0    
        T=float('inf')
        while i < rounds:
            if self.State.isEnd:
                print("Number of moves done to reach goal state")
                self.pathslength.append(len(self.path))
                print(self.pathslength[len(self.pathslength)-1])
                T = len(self.states)
                tau = len(self.path) - self.bootstrap
                if tau >=0 :
                    G = 0 
                    for k in range(tau + 1, min(tau + self.bootstrap,T)):
                        G += pow(self.gamma,k-tau-1)*self.rewards[k]
                        if tau + self.bootstrap < T:
                            G += pow(self.gamma,self.bootstrap)*self.getQ(self.states[tau+self.bootstrap],self.path[tau+self.bootstrap-1])
                            self.learnQ(self.states[tau],self.path[tau],G)
                self.reset()
                i += 1
            else:
                action = self.chooseAction(self.State.state)
                self.states.append(self.State.nxtPosition(action))
                self.path.append(action)
                self.State = self.takeAction(action)
                self.rewards.append(self.State.giveReward())
                tau = len(self.path) - self.bootstrap
                if tau >=0 :
                    G = 0 
                    for k in range(tau + 1, min(tau + self.bootstrap,T)):
                        G += pow(self.gamma,k-tau-1)*self.rewards[k]
                    if tau + self.bootstrap < T:
                        G += pow(self.gamma,self.bootstrap)*self.getQ(self.states[tau+self.bootstrap],self.path[tau+self.bootstrap-1])
                        self.learnQ(self.states[tau],self.path[tau],G)
                self.State.isEndFunc()        
                    

    def showPolicy(self):
        for i in range(0, BOARD_ROWS):
            print('----------------------------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                state = (i,j)
                q = [self.getQ(state, a) for a in self.State.actions]
                maxQ = max(q)
                count = q.count(maxQ)
                if count > 1:
                    best = [i for i in range(len(self.State.actions)) if q[i] == maxQ]
                    i = np.random.choice(best)
                else:
                    i = q.index(maxQ)

                action = self.State.actions[i]
                out += str(action + ' | ')
            print(out)
        print('----------------------------------')
        x=range(len(self.pathslength))
        y=self.pathslength
        y_last=y[len(y)-100:len(y)-1]
        print(mean(y_last))
        plt.yscale('log')
        plt.plot(x,y)
        plt.xlabel("Episode")
        plt.ylabel("Number of moves")
        plt.title("Evolution of the number of moves to reach goal state in function of the learning episode")


if __name__ == "__main__":
    ag = Agent()
    ag.play(200)
    print(ag.showPolicy())
