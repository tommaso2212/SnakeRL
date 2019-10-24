# This class contains the statical variables which are used in this project
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
	OBJ_TAIL = 3
	OBJ_FRUIT = 4
	'''
	Rewards:
		+5 - eat fruit
		-1 - death
		-0.1 - else
	'''
	REWARD_FRUIT = 1
	REWARD_LOSE = -1
	REWARD_ELSE = -0.01
	'''
	Actions:
		0 - straight movement
		1 - left movement
		2 - right movement
	'''
	MOVEMENT_STRAIGHT = 0
	MOVEMENT_LEFT = 1
	MOVEMENT_RIGHT = 2
	'''
	Q Learning parameters
	'''
	GAMMA = 0.9  # Discount factor
	ALPHA = 0.01   # Learning rate
	'''
	Epsilon greedy policy
	'''
	EPSILON_MAX = 0.5   
	EPSILON_MIN = 0.1
	EPSILON_DECREASE = 0.05
