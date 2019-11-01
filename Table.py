##
# This class defines the space state and the action space
##


import numpy as np
import pandas as pd

class Table:

    def __init__(self, state, actions=None):
        '''
    	State:
        	state[0] - Wall in the cell upward of Snake's head
        	state[1] - Wall in the cell to the left of Snake's head
        	state[2] - Wall in the cell to the right of Snake's head
		state[3] - Wall in the cell downward of Snake's head
        	state[4] - Fruit position upward or downward with respect to the head
        	state[5] - Fruit position to the left or to the right with respect to the head
    	'''
        self.state = np.array(state, dtype=int)
        '''
            actions[0] - Upward movement
            actions[1] - Left movement
            actions[2] - Right movement
            actions[3] - Downward movement
        '''
        self.actions = np.zeros(4, dtype=float)
        if actions is not None:
            #print(actions)
            self.actions = actions

    def getAction(self):
        return np.argmax(self.actions)
