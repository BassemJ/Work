# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 17:32:59 2019

@author: BassemJ
"""

import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import time as t

BOARD_ROWS = 7
BOARD_COLS = 10
WIN_STATE = (3, 7)
START = (3, 0)
WIND = [0,0,0,1,1,1,2,2,1,0]

class State:
    def __init__(self, state=START):
        self.state = state
        self.actions = [ "down","up", "left", "right"]
        self.AllStates = [(0, 0),(0, 1),(0, 2),(0, 3),(0, 4),(0, 5),(0, 6),(0, 7),(0, 8),(0, 9),
                          (1, 0),(1, 1),(1, 2),(1, 3),(1, 4),(1, 5),(1, 6),(1, 7),(1, 8),(1, 9),
                          (2, 0),(2, 1),(2, 2),(2, 3),(2, 4),(2, 5),(2, 6),(2, 7),(2, 8),(2, 9),
                          (3, 0),(3, 1),(3, 2),(3, 3),(3, 4),(3, 5),(3, 6),(3, 7),(3, 8),(3, 9),
                          (4, 0),(4, 1),(4, 2),(4, 3),(4, 4),(4, 5),(4, 6),(4, 7),(4, 8),(4, 9),
                          (5, 0),(5, 1),(5, 2),(5, 3),(5, 4),(5, 5),(5, 6),(5, 7),(5, 8),(5, 9),
                          (6, 0),(6, 1),(6, 2),(6, 3),(6, 4),(6, 5),(6, 6),(6, 7),(6, 8),(6, 9)]
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
        self.pathslength = []
        self.State = State()
        self.path = [np.random.choice(self.State.actions)]
        self.epsilon = 0.1
        self.alpha = 0.4
        self.gamma = 0.99
        self.l = 0.94
        self.q = {}
        self.e = {}

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)
    
    def getE(self, state, action):
        return self.e.get((state, action), 0.0)

    def initE(self):
        for k in range(7) : 
                    for l in range(10) :
                        for a in self.State.actions:
                                self.e[(k,l),a] = 0.0
                        
    def initQ(self):
        for k in range(7) : 
                    for l in range(10) :
                        for a in self.State.actions:
                                self.q[(k,l),a] = 0.0
        
    
    def learnQ(self, state, action, delta, E):
        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = self.alpha * delta * E 
        else:
            self.q[(state, action)] = oldv + self.alpha * delta * E
    
    def incrementE(self, state, action):
        oldv = self.e.get((state, action), None)
        if oldv is None:
            self.e[(state, action)] = 1
        else:
            self.e[(state, action)] = oldv + 1
            
    def multiplyE(self, state, action):
        oldv = self.getE(state,action)
        self.e[(state, action)] = self.gamma*self.l*oldv

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
        self.State = State()
        self.path = [np.random.choice(self.State.actions)]
        self.initE()
        self.initQ()

    def play(self, rounds):
        i = 0
        self.initE()
        self.initQ()
#        step_count = 0
        while i < rounds:
            if self.State.isEnd:
                print("Number of moves done to reach goal state")
                self.pathslength.append(len(self.path))
                print(self.pathslength[len(self.pathslength)-1])
                reward = self.State.giveReward()
                self.rewards.append(reward)
                self.reset()
                i += 1
            else:
                reward = self.State.giveReward()
                action1 = self.path[len(self.path) - 1]
                self.states.append(self.State.nxtPosition(action1))
                self.State = self.takeAction(action1)
                self.rewards.append(reward)
                action2 = self.chooseAction(self.State.state)
                self.incrementE(self.states[len(self.states)-2],action1)
                delta = reward + self.gamma*(self.getQ(self.states[len(self.states) - 1],action2) - self.getQ(self.states[len(self.states)-2],action1)) 
                for k in range(7) : 
                    for l in range(10) :
                        for a in self.State.actions:
                            self.learnQ(self.State.AllStates[k*10+l],a,delta,self.getE(self.State.AllStates[k*10+l],a))
                            self.multiplyE(self.State.AllStates[k],a)
                self.path.append(action2)
                print(action1, self.State.state)
#                step_count += 1
#                print(step_count)
#                print(len(self.path))
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
        print(self.q)
        plt.yscale('log')
        plt.plot(x,y)
        plt.xlabel("Episode")
        plt.ylabel("Number of moves")
        plt.title("Evolution of the number of moves to reach goal state in function of the learning episode")


if __name__ == "__main__":
    timer = t.time()
    ag = Agent()
    ag.play(10)
    print(ag.showPolicy())
    print(t.time()-timer)