##
#	Description of project
##

from GameEngine import GameEngine
from State import State
from Parameters import Parameters
import numpy as np
import random
import pandas as pd
import sys

class Snake:

	def __init__(self):
		self.engine = GameEngine()
		self.EPOCHS = 80
		self.resultsDF = pd.DataFrame(columns=['EPOCH', 'POINTS', 'REWARD'])

	def playQNAgent(self, path=None, graphics=None):
		from QNAgent import QNAgent
		agent = QNAgent(path)
		epsilon = Parameters.EPSILON_MAX
		if graphics:
			print("Not yet")
		else:
			for i in range(0, self.EPOCHS):
				points = 0  # Sum of points
				tot_reward = 0  # Sum of rewards
				self.engine.newGame()	# Start new game
				game_over = False	# Flag of game over
				while not game_over:
					reward = self.QAgent(epsilon, agent)
					tot_reward += reward 	# Sum reward
					if reward == Parameters.REWARD_LOSE:	# If True the snake is died
						game_over = True
					elif reward == Parameters.REWARD_FRUIT:	# If True the snake has eaten a fruit
						points += 1	# Sum points
				# Update epsilon value
				if epsilon > Parameters.EPSILON_MIN:
					epsilon -= Parameters.EPSILON_DECREASE
				else:
					epsilon = Parameters.EPSILON_MIN
				self.progress(i)
				self.addToDF(i, points, tot_reward, 'QNresults.csv')
			agent.saveTable()

	def QAgent(self, epsilon, agent):
		old_state = State.getState(self.engine)	# Get actual state
		# Choose action with epsilon-greedy policy
		if random.random() < epsilon:
			action = random.randint(0, 2)
		else:
			action = agent.getAction(old_state)
		reward = self.engine.executeAction(action)	# Execute action and gain the reward
		new_state = State.getState(self.engine)	# Get state after the action
		agent.updateQTable(old_state, new_state, action, reward)	# Update Q-Table
		return reward

	def playDQNAgent(self, weights=None, graphics=False):
		from DQNAgent import DQNAgent
		agent = DQNAgent(weights)
		epsilon = Parameters.EPSILON_MAX
		if graphics:
			print("not yet")
		else:
			for i in range(0, self.EPOCHS):
				points = 0  # Sum of points
				tot_reward = 0  # Sum of rewards
				self.engine.newGame()
				game_over = False
				while not game_over:
					old_state = State.getState(self.engine)	# Get actual state
					# Choose action with epsilon-greedy policy
					if random.random() < epsilon:
						action = agent.getAction(old_state, random_value=1)
					else:
						action = agent.getAction(old_state)
					reward = self.engine.executeAction(np.argmax(action))	# Execute action and get reward
					new_state = State.getState(self.engine)	# Get new state
					# Update sum rewards and points
					tot_reward += reward
					if reward == Parameters.REWARD_LOSE:
						game_over = True
					elif reward == Parameters.REWARD_FRUIT:
						points += 1
					# Train Agent
					agent.inGameTraining(old_state, action, reward, new_state, game_over)
				# Update epsilon value
				if epsilon > Parameters.EPSILON_MIN:
					epsilon -= Parameters.EPSILON_DECREASE
				else:
					epsilon = Parameters.EPSILON_MIN
				# Train agent using memory
				agent.batchTraining()
				self.addToDF(i, points, tot_reward, 'DQNresults.csv')
				self.progress(i)
		agent.model.save_weights('weights.hdf5')

	# Add game stats to dataframe
	def addToDF(self, epoch, points, reward, path):
		self.resultsDF = self.resultsDF.append({'EPOCH': epoch, 'POINTS': points, 'REWARD': reward}, ignore_index=True)
		self.resultsDF.to_csv(repr(path))

	def progress(self, epoch):
		sys.stdout.write("\rProgress: " + str(epoch))
		sys.stdout.flush()

def printInstructions():
	print("\nInstructions:")
	print("\n\tPlay Deep Q Learning - python Snake.py -dqn\n\tPlay Deep Q Learning with graphic view - python Snake.py -dqng")
	print("\n\tPlay Q Learning - python Snake.py -qn\n\tPlay Q Learning with graphic view - python Snake.py -qng")
	print("\n")

# Checks arguments
if len(sys.argv) > 1:
	if sys.argv[1] == "-dqng":
		snake = Snake()
		snake.playDQNAgent(graphics=True)
	elif sys.argv[1] == "-dqn":
		snake = Snake()
		snake.playDQNAgent() 
	elif sys.argv[1] == "-qng":
		snake = Snake()
		snake.playQNAgent(graphics=True)
	elif sys.argv[1] == "-qn":
		snake = Snake()
		snake.playQNAgent()
	else:
		printInstructions()
else:
	printInstructions()