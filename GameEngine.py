##
#	This class is the core of the game.
#	It defines defines the rules and manages the game.
##

import random
import numpy as np
from Parameters import Parameters as par

class GameEngine:

	def __init__(self):
		self.endGame = False

    # Method to initialize a new game
	def newGame(self):
		# Generate playground as a matrix
		self.playground = np.zeros([par.PLAYGROUND_WIDTH, par.PLAYGROUND_HEIGHT])
		# The snake is a list of Body's objects
		self.snake = []
		self.snake.append(Body(15, 10, par.OBJ_HEAD))
		self.snake.append(Body(16, 10, par.OBJ_BODY))
		self.snake.append(Body(17, 10, par.OBJ_BODY))
		# Update playground matrix replacing zeros with snake's values
		self.updatePlayground()
		# Generate and put a fruit inside the playground 
		self.endGame = self.genFruit()

    # Update playground's values
	def updatePlayground(self):
		# Set all the values to 0
		self.playground[:, :] = 0
		# Replace values with snake's ones
		for i in range(0, len(self.snake)):
			self.playground[self.snake[i].position_x, self.snake[i].position_y] = self.snake[i].obj_value

    # Random generate of a fruit in the playground
	def genFruit(self):
		# Checks empty cell
		x, y = self.find(0)
		if x is None or y is None:
			return True
		else:
			# Generate random position for the fruit until it is placed into an empty position
			while True:
				x_fruit = random.randint(0, par.PLAYGROUND_WIDTH - 1)
				y_fruit = random.randint(0, par.PLAYGROUND_HEIGHT - 1)
				if self.isFree(x_fruit, y_fruit):	# True if the fruit is not over the snake
					break
			# Put the fruit in the playground
			self.playground[x_fruit, y_fruit] = par.OBJ_FRUIT
			return False

	# Return True if the position is not occupied by the snake
	def isFree(self, x, y):
		if self.playground[x, y] == 0:
			return True
		else:
			return False

	# Return the position of an object inside the playground
	def find(self, obj):
		x = None
		y = None
		for i in range(0, par.PLAYGROUND_WIDTH):
			for j in range(0, par.PLAYGROUND_HEIGHT):
				if self.playground[i, j] == obj:
					x, y = i, j
		return x, y
	
	def executeAction(self, action):
        # Find position of the head
		x_head, y_head = self.find(par.OBJ_HEAD)
        # Find new position of the head
		if action == 0:
			new_x_head, new_y_head = x_head, y_head -1
		elif action == 1:
			new_x_head, new_y_head = x_head - 1, y_head
		elif action == 2:
			new_x_head, new_y_head = x_head + 1, y_head
		elif action == 3:
			new_x_head, new_y_head = x_head, y_head + 1
        # Execute movement and return reward
		if new_x_head < 0 or new_x_head > par.PLAYGROUND_WIDTH -1 or new_y_head < 0 or new_y_head > par.PLAYGROUND_HEIGHT - 1:
			return par.REWARD_LOSE  # Hits one wall
		else:
			obj = self.playground[new_x_head, new_y_head]
			if obj == par.OBJ_BODY:
				return par.REWARD_LOSE  # Hits his body
			elif obj == par.OBJ_FRUIT:  # Eats a fruit
                # Add new piece to the snake
				self.snake.append(Body(self.snake[len(self.snake) - 1].position_x, self.snake[len(self.snake) - 1].position_y, par.OBJ_BODY))
				# Update positions
				for i in range(len(self.snake) - 2, 0, -1):
					self.snake[i].position_x = self.snake[i - 1].position_x
					self.snake[i].position_y = self.snake[i - 1].position_y
				self.snake[0].position_x = new_x_head
				self.snake[0].position_y = new_y_head
				self.updatePlayground()
				self.endGame = self.genFruit()
				return par.REWARD_FRUIT
			else:   # Goes in an empty cell
                # Update positions
				for i in range(len(self.snake) - 1, 0, -1):
					self.snake[i].position_x = self.snake[i - 1].position_x
					self.snake[i].position_y = self.snake[i - 1].position_y
				self.snake[0].position_x = new_x_head
				self.snake[0].position_y = new_y_head
				x_fruit, y_fruit = self.find(par.OBJ_FRUIT)
				self.updatePlayground()
				self.playground[x_fruit, y_fruit] = par.OBJ_FRUIT
				return par.REWARD_ELSE
	'''
    	State:
        	state[0] - Wall in the cell upward of Snake's head
        	state[1] - Wall in the cell to the left of Snake's head
        	state[2] - Wall in the cell to the right of Snake's head
		state[3] - Wall in the cell downward of Snake's head
        	state[4] - Fruit position upward or downward with respect to the head
        	state[5] - Fruit position to the left or to the right with respect to the head
    	'''
	def getState(self):
		state = np.zeros(6, dtype=int)
		# Find snake's head
		x_head, y_head = self.find(par.OBJ_HEAD)
		# Danger in the cell upward
		state[0] = self.dangerNear(x_head, y_head - 1)
		# Danger in the cell to the left
		state[1] = self.dangerNear(x_head - 1, y_head)
		# Danger in the cell to the right
		state[2] = self.dangerNear(x_head + 1, y_head)
		# Danger in the cell downward
		state[3] = self.dangerNear(x_head, y_head + 1)
		# Find fruit
		x_fruit, y_fruit = self.find(par.OBJ_FRUIT)
		if x_fruit is None or y_fruit is None:
			x_fruit, y_fruit = x_head, y_head
		if y_head > y_fruit:
			state[4] = -1    # Fruit upward
		elif y_head < y_fruit:
			state[4] = 1    # Fruit downward
		if x_head > x_fruit:
			state[5] = -1    # Fruit to the left
		elif x_head < x_fruit:
			state[5] = 1    # Fruit to the right
		# Return state
		return state
	
	def dangerNear(self, new_x_head, new_y_head):
		if new_x_head < 0 or new_x_head > par.PLAYGROUND_WIDTH -1 or new_y_head < 0 or new_y_head > par.PLAYGROUND_HEIGHT - 1:
			return 1    # Wall
		elif self.playground[new_x_head, new_y_head] == par.OBJ_BODY:
			return 1    # Body
		else:
			return 0    # No danger

'''
Each object of this class is one piece of the snake
'''
class Body:
	def __init__(self, position_x, position_y, obj_value):
		self.position_x = position_x
		self.position_y = position_y
		self.obj_value = obj_value
