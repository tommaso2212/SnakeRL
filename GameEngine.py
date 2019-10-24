##
#	This class is the core of the game.
#	It defines defines the rules and manages the game.
##

import random
import numpy as np
from Parameters import Parameters

class GameEngine:

	# Method to initialize a new game
	def newGame(self):
		# Generate playground as a matrix
		self.playground = np.zeros([Parameters.PLAYGROUND_WIDTH, Parameters.PLAYGROUND_HEIGHT])
		# The snake is a list of Body's objects
		self.snake = []
		self.snake.append(Body(14, 10, Parameters.OBJ_HEAD))
		self.snake.append(Body(15, 10, Parameters.OBJ_BODY))
		self.snake.append(Body(16, 10, Parameters.OBJ_TAIL))
		# Update playground matrix replacing zeros with snake's values
		self.updatePlayground()
		# Generate and put a fruit inside the playground 
		self.genFruit()
		# At the beginning, the snake moves to the left
		self.direction = "left"

	# Update playground's values
	def updatePlayground(self):
		# Set all the values to 0
		self.playground[:, :] = 0
		# Replace values with snake's ones
		for i in range(0, len(self.snake)):
			self.playground[self.snake[i].position_x, self.snake[i].position_y] = self.snake[i].obj_value

	# Random generate of a fruit in the playground
	def genFruit(self):
		# Generate random position for the fruit until it is placed into an empty position
		while True:
			x_fruit = random.randint(0, Parameters.PLAYGROUND_WIDTH - 1)
			y_fruit = random.randint(0, Parameters.PLAYGROUND_HEIGHT - 1)
			if self.isFree(x_fruit, y_fruit):	# True if the fruit is not over the snake
				break
		# Put the fruit in the playground
		self.playground[x_fruit, y_fruit] = Parameters.OBJ_FRUIT

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
		for i in range(0, Parameters.PLAYGROUND_WIDTH):
			for j in range(0, Parameters.PLAYGROUND_HEIGHT):
				if self.playground[i, j] == obj:
					x, y = i, j
		return x, y

	# Executes an action and returns a reward
	def executeAction(self, action_value):
		# Find actual values
		x_head, y_head = self.find(Parameters.OBJ_HEAD)
		# Find new values
		if self.direction == "up":
			new_x_head, new_y_head = self.upMovement(action_value, x_head, y_head)
		elif self.direction == "left":
			new_x_head, new_y_head = self.leftMovement(action_value, x_head, y_head)
		elif self.direction == "right":
			new_x_head, new_y_head = self.rightMovement(action_value, x_head, y_head)
		elif self.direction == "down":
			new_x_head, new_y_head = self.downMovement(action_value, x_head, y_head)

		# Execute the movement and return reward
		if new_x_head < 0 or new_x_head > Parameters.PLAYGROUND_WIDTH - 1 or new_y_head < 0 or new_y_head > Parameters.PLAYGROUND_HEIGHT - 1:  # Hits one wall
			return Parameters.REWARD_LOSE
		else:
			obj = self.playground[new_x_head, new_y_head]
			if obj == Parameters.OBJ_BODY or obj == Parameters.OBJ_TAIL:  # Hits his body
				return Parameters.REWARD_LOSE
			elif obj == Parameters.OBJ_FRUIT:  # Eats the fruit
				self.snake[len(self.snake) - 1].value = Parameters.OBJ_BODY
				self.snake.append(Body(10, 10, Parameters.OBJ_TAIL))
				for i in range(len(self.snake) - 1, 0, -1):
					self.snake[i].position_x = self.snake[i - 1].position_x
					self.snake[i].position_y = self.snake[i - 1].position_y
				self.snake[0].position_x = new_x_head
				self.snake[0].position_y = new_y_head
				self.updatePlayground()
				self.genFruit()
				return Parameters.REWARD_FRUIT
			else:  # Else
				for i in range(len(self.snake) - 1, 0, -1):
					self.snake[i].position_x = self.snake[i - 1].position_x
					self.snake[i].position_y = self.snake[i - 1].position_y
				self.snake[0].position_x = new_x_head
				self.snake[0].position_y = new_y_head
				x_fruit, y_fruit = self.find(Parameters.OBJ_FRUIT)
				self.updatePlayground()
				self.playground[x_fruit, y_fruit] = Parameters.OBJ_FRUIT
				return Parameters.REWARD_ELSE

	# Returns the new positions of snake's head if it's direction was upward
	def upMovement(self, action_value, x_head, y_head):
		if action_value == 0:
			new_x_head, new_y_head = x_head, y_head - 1
		elif action_value == 1:
			new_x_head, new_y_head = x_head - 1, y_head
			self.direction = "left"
		elif action_value == 2:
			new_x_head, new_y_head = x_head + 1, y_head
			self.direction = "right"
		return new_x_head, new_y_head

	# Returns the new positions of snake's head if it's direction was to the left
	def leftMovement(self, action_value, x_head, y_head):
		if action_value == 0:
			new_x_head, new_y_head = x_head - 1, y_head
		elif action_value == 1:
			new_x_head, new_y_head = x_head, y_head + 1
			self.direction = "down"
		elif action_value == 2:
			new_x_head, new_y_head = x_head, y_head - 1
			self.direction = "up"
		return new_x_head, new_y_head

	# Returns the new positions of snake's head if it's direction was to the right
	def rightMovement(self, action_value, x_head, y_head):
		if action_value == 0:
			new_x_head, new_y_head = x_head + 1, y_head
		elif action_value == 1:
			new_x_head, new_y_head = x_head, y_head - 1
			self.direction = "up"
		elif action_value == 2:
			new_x_head, new_y_head = x_head, y_head + 1
			self.direction = "down"
		return new_x_head, new_y_head

	# Returns the new positions of snake's head if it's direction was downward
	def downMovement(self, action_value, x_head, y_head):
		if action_value == 0:
			new_x_head, new_y_head = x_head, y_head + 1
		elif action_value == 1:
			new_x_head, new_y_head = x_head + 1, y_head
			self.direction = "right"
		elif action_value == 2:
			new_x_head, new_y_head = x_head - 1, y_head
			self.direction = "left"
		return new_x_head, new_y_head

'''
Each object of this class is one piece of the snake
'''
class Body:
	def __init__(self, position_x, position_y, obj_value):
		self.position_x = position_x
		self.position_y = position_y
		self.obj_value = obj_value