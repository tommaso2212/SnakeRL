##
# This class define and manage DQN Agent for the game
##

from Parameters import Parameters as par
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.utils import to_categorical

class DeepQLearning:

    def __init__(self, weights=None):
        self.memory = deque(maxlen=2000)
        self.model = self.createModel(weights)

    # Create model
    def createModel(self, weights):
        model = Sequential()
        model.add(Dense(64, input_dim = 6, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(4, activation='softmax'))
        model.compile(loss='mse', optimizer=Adam(lr=par.ALPHA))
        if weights:
            model.load_weights(weights)
        return model

    # Add transition to memory
    def addToMemory(self, old_state, action, reward, new_state, game_over):
        self.memory.append((old_state, action, reward, new_state, game_over))

    # Train the model using minibatch
    def minibatchTraining(self):
        if len(self.memory) > 64:
            minibatch = random.sample(self.memory, 10)
        else:
            minibatch = self.memory
        for old_state, action, reward, new_state, game_over in minibatch:
            if game_over:
                q_value = reward
            else:
                q_value = (reward + par.GAMMA * np.amax(self.model.predict(new_state.reshape(1,6))[0]))
            q_table = self.model.predict(old_state.reshape(1,6))[0]
            q_table[np.argmax(action)] = q_value
            self.model.fit(old_state.reshape(1,6), q_table.reshape(1,4), epochs=1, verbose=0)
    
    # Return Q-values for all possible actions
    def getAction(self, old_state):
        return self.model.predict(old_state.reshape(1,6))

    # Save model
    def saveTable(self):
        self.model.save_weights('weights.hdf5')
    
