###
# This class define a State of the environment
###

from GameEngine import GameEngine
from Parameters import Parameters
import numpy as np


class State:

	'''
	State:
		state[0] - Wall in the cell in front of Snake's head
		state[1] - Wall in the cell to the left of Snake's head
		state[2] - Wall in the cell to the right of Snake's head
		state[3] - Fruit position upward with respect to the head
		state[4] - Fruit position to the left with respect to the head
		state[5] - Fruit position to the right with respect to the head
		state[6] - Fruit position downward with respect to the head
		state[7] - Direction of movement
	'''
	@staticmethod
	def getState(gameEngine):
		state = [0, 0, 0, 0, 0, 0, 0]
		x_head, y_head = gameEngine.find(Parameters.OBJ_HEAD)

		# Wall in the cell near Snake's head
		if gameEngine.direction == "up":
			new_x, new_y = gameEngine.upMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[0] = 1
			new_x, new_y = gameEngine.leftMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[1] = 1
			new_x, new_y = gameEngine.rightMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[2] = 1
		elif gameEngine.direction == "left":
			new_x, new_y = gameEngine.leftMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[0] = 1
			new_x, new_y = gameEngine.downMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[1] = 1
			new_x, new_y = gameEngine.upMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[2] = 1
		elif gameEngine.direction == "right":
			new_x, new_y = gameEngine.rightMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[0] = 1
			new_x, new_y = gameEngine.upMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[1] = 1
			new_x, new_y = gameEngine.downMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[2] = 1
		elif gameEngine.direction == "down":
			new_x, new_y = gameEngine.downMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[0] = 1
			new_x, new_y = gameEngine.rightMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[1] = 1
			new_x, new_y = gameEngine.leftMovement(0, x_head, y_head)
			if new_x < 0 or new_x > Parameters.PLAYGROUND_WIDTH - 1 or new_y < 0 or new_y > Parameters.PLAYGROUND_HEIGHT - 1 or \
					gameEngine.playground[new_x, new_y] == Parameters.OBJ_BODY or gameEngine.playground[new_x, new_y] == Parameters.OBJ_TAIL:
				state[2] = 1

		# Relative position of the fruit with respect to the head
		x_fruit, y_fruit = gameEngine.find(Parameters.OBJ_FRUIT)	
		if y_fruit > y_head:    # If True the fruit is downward with respect to the head
			state[6] = 1#fruit down
		else:
			state[3] = 1#fruit up
		if x_fruit > x_head:    # If True the fruit is to the right with respect to the head
			state[5] = 1  # right
		else:
			state[4] = 1#left
		'''
		if gameEngine.direction == "up":
			state[5] = 0
		elif gameEngine.direction == "left":
			state[5] = 1
		elif gameEngine.direction == "right":
			state[5] = 2
		elif gameEngine.direction == "down":
			state[5] = 3
		'''
		# Return state
		return np.asarray(state)
