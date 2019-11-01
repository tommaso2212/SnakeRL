##
# This class contains the statical variables which are used in this project
##


class Parameters:
	'''
	Playground dimensions
	'''
	PLAYGROUND_WIDTH = 20
	PLAYGROUND_HEIGHT = 20
	'''
	Game's object in the playground:
		0 - empty cell
		1 - head
		2 - body
		3 - tail
	4 - fruit
	'''
	OBJ_HEAD = 1
	OBJ_BODY = 2
	OBJ_FRUIT = 4
	'''
	Rewards:
		+5 - eat fruit
		-1 - death
		-0.025 - else
	'''
	REWARD_FRUIT = 5
	REWARD_LOSE = -1
	REWARD_ELSE = -0.025
	'''
	Actions:
		0 - straight movement
		1 - left movement
		2 - right movement
	'''
	MOVEMENT_UPWARD = 0
	MOVEMENT_LEFT = 1
	MOVEMENT_RIGHT = 2
	MOVEMENT_DOWNWARD = 3
	'''
	Q Learning parameters
	'''
	GAMMA = 0.9  # Discount factor
	ALPHA = 0.0005   # Learning rate
	'''
	Epsilon greedy policy
	'''
	EPSILON_MAX = 0.4   
	EPSILON_MIN = 0.05
	EPSILON_DECREASE = 0.005
