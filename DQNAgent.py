##
# This class define and manage DQN Agent for the game
##

from Parameters import Parameters
import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.utils import to_categorical

class DQNAgent:

	def __init__(self, weights=None):
		self.memory = []
		self.model = self.createModel(weights)

	# Create DQN model using Keras
	def createModel(self, weights):
		model = Sequential()
		model.add(Dense(30, input_dim=7, activation='relu'))
		model.add(Dropout(0.15))
		model.add(Dense(30, activation='relu'))
		model.add(Dropout(0.15))
		model.add(Dense(90, activation='relu'))
		model.add(Dropout(0.15))
		model.add(Dense(3, activation='linear'))
		model.compile(loss='mse', optimizer=Adam(lr=Parameters.ALPHA))
		if weights:
			model.load_weights(weights)
		return model

	# Add new item to the memory
	def addToMemory(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))

	# Train the network at each movement
	def inGameTraining(self, state, action, reward, next_state, done):
		if done:
			q_value = reward
		else:
			q_value = reward + Parameters.GAMMA * np.amax(self.model.predict(next_state.reshape((1, 7)))[0])
		q_table = self.model.predict(state.reshape((1, 7)))
		q_table[0][np.argmax(action)] = q_value
		self.model.fit(state.reshape((1, 7)), q_table, epochs=1, verbose=0)
		self.addToMemory(state, action, reward, next_state, done)		

	# Train the network using memory
	def batchTraining(self):
		print("\n", len(self.memory))
		if len(self.memory) > 500:
			batch = random.sample(self.memory, 500)
		else:
			batch = self.memory
		for state, action, reward, next_state, done in batch:
			if done:
				q_value = reward
			else:
				q_value = (reward + Parameters.GAMMA * np.amax(self.model.predict(next_state.reshape(1, 7))[0]))
			q_table = self.model.predict(state.reshape(1, 7))
			q_table[0][np.argmax(action)] = q_value
			self.model.fit(state.reshape(1, 7), q_table, epochs=1, verbose=0)

	def getAction(self, old_state, random_value=None):
		if random_value:
			return random.randint(0, 2)
		action = self.model.predict(old_state.reshape(1, 7))
		return np.argmax(action[0])
