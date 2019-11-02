##
#	Description of project
##

from Parameters import Parameters as par
from GameEngine import GameEngine
import numpy as np
import random
import pandas as pd
import sys

class Snake:
    def __init__(self):
        self.engine = GameEngine()
        self.EPOCHS = 100000  # Number of matches
        self.resultsDF = pd.DataFrame(columns=['EPOCH', 'POINTS', 'REWARD'])

    # Print progress
    def progress(self, epoch):
        sys.stdout.write("\rProgress: " + str(epoch) + "/" + str(self.EPOCHS))
        sys.stdout.flush()

    # Play Snake using Q Learning
    def playQNAgent(self, userView=None):
        from QLearning import QLearning
        agent = QLearning() # QLearning(path) for load Q-Table
        epsilon = par.EPSILON_MAX
        if userView:
            from UserView import UserView
            graphic = UserView()
        for i in range(0, self.EPOCHS):
            points = 0  # Sum of points
            tot_reward = 0  # Sum of rewards
            self.engine.newGame()	# Start new game
            game_over = False	# Flag of game over
            while not game_over:
                if userView:
                    graphic.draw(self.engine.playground)
                old_state = self.engine.getState() # Get actual state
                # Choose action with epsilon-greedy policy
                if random.random() < epsilon:
                    action = random.randint(0, 3)
                else:
                    action = agent.getAction(old_state)
                reward = self.engine.executeAction(action)	# Execute action and gain the reward
                new_state = self.engine.getState()	# Get state after the action
                agent.updateTable(old_state, new_state, action, reward)	# Update Q-Table
                tot_reward += reward 	# Sum reward
                if reward == par.REWARD_LOSE or self.engine.endGame:	# If True the snake is died
                    game_over = True
                elif reward == par.REWARD_FRUIT:	# If True the snake has eaten a fruit
                    points += 1	# Sum points
			# Update epsilon value
            if epsilon > par.EPSILON_MIN:
                epsilon -= par.EPSILON_DECREASE
            else:
                epsilon = par.EPSILON_MIN
            self.progress(i)
            self.resultsDF = self.resultsDF.append({'EPOCH': i, 'POINTS': points, 'REWARD': tot_reward}, ignore_index=True)
            self.resultsDF.to_csv(r"QNresults.csv")
        if userView:
            graphic.close()
        agent.saveTable()
    
    # Play Snake using Deep Q Learning
    def playDQNAgent(self, userView=None):
        from DeepQLearning import DeepQLearning
        agent = DeepQLearning() # DeepQLearning(path) to load weights
        epsilon = par.EPSILON_MAX
        if userView:
            from UserView import UserView
            graphic = UserView()
        for i in range(0, self.EPOCHS):
            points = 0  # Sum of points
            tot_reward = 0  # Sum of rewards
            self.engine.newGame()	# Start new game
            game_over = False	# Flag of game over
            while not game_over:
                if userView:
                    graphic.draw(self.engine.playground)
                old_state = self.engine.getState() # Get actual state
                # Choose action with epsilon-greedy policy
                if random.random() < epsilon:
                    action_value = random.randint(0, 3)
                    action = np.zeros(4, dtype=int)
                    action[action_value] = 1
                else:
                    action = agent.getAction(old_state)
                    action_value = np.argmax(action)
                reward = self.engine.executeAction(action_value)	# Execute action and gain the reward
                new_state = self.engine.getState()	# Get state after the action
                agent.addToMemory(old_state, action, reward, new_state, game_over)	# Update Q-Table
                tot_reward += reward 	# Sum reward
                if reward == par.REWARD_LOSE or self.engine.endGame:	# If True the snake is died
                    game_over = True
                elif reward == par.REWARD_FRUIT:	# If True the snake has eaten a fruit
                    points += 1	# Sum points
            agent.minibatchTraining()
			# Update epsilon value
            if epsilon > par.EPSILON_MIN:
                epsilon -= par.EPSILON_DECREASE
            else:
                epsilon = par.EPSILON_MIN
            self.progress(i)
            self.resultsDF = self.resultsDF.append({'EPOCH': i, 'POINTS': points, 'REWARD': tot_reward}, ignore_index=True)
            self.resultsDF.to_csv(r"DQNresults2.csv")
        if userView:
            graphic.close()
        agent.saveTable()   



def printInstructions():
	print("\nInstructions:")
	print("\n\tPlay Deep Q Learning - python Snake.py -dqn\n\tPlay Deep Q Learning with graphic view - python Snake.py -dqng")
	print("\n\tPlay Q Learning - python Snake.py -qn\n\tPlay Q Learning with graphic view - python Snake.py -qng")
	print("\n")

# Checks arguments
if len(sys.argv) > 1:
    if sys.argv[1] == "-dqng":
        snake = Snake()
        snake.playDQNAgent(userView=True)
    elif sys.argv[1] == "-dqn":
        snake = Snake()
        snake.playDQNAgent() 
    elif sys.argv[1] == "-qng":
        snake = Snake()
        snake.playQNAgent(userView=True)
    elif sys.argv[1] == "-qn":
        snake = Snake()
        snake.playQNAgent()
    else:
        printInstructions()
else:
    printInstructions()
