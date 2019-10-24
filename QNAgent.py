##
# This class define and manage Q-Agent for the game
##

import json
import numpy as np
from Parameters import Parameters

class QNAgent:

	def __init__(self, path=None):
		self.q_table = {}
		self.q_table['state'] = []
		if path is not None:
			self.loadTable(path)

	def getAction(self, state):
		return np.argmax(self.getItem(state)['action'])

	def updateQTable(self, old_state, new_state, action, reward):
		self.getItem(old_state)['action'][action] = float(self.getItem(old_state)['action'][action] + Parameters.ALPHA * (reward + Parameters.GAMMA * np.max(self.getItem(new_state)['action']) - self.getItem(old_state)['action'][action]))

	# Tries to load the table from a file, if the file not exists it creates an empty new one and then loads an empty table
	def loadTable(self, path):
		try:
			with open(path) as file:
				self.q_table = json.load(file)
		except:
			self.saveTable(path)
			with open(path) as file:
				self.q_table = json.load(file)

	# Opens json file and saves q table inside
	def saveTable(self, path=None):
		if path is None:
			path = 'q_table.json'
		with open(path, 'w') as file:
			json.dump(self.q_table, file)

	# Add a new raw to Q-Table
	def addNewItem(self, state, straight, left, right):
		item = {
			'danger_straight': int(state[0]),
			'danger_left': int(state[1]),
			'danger_right': int(state[2]),
			'fruit_up': int(state[3]),
			'fruit_left': int(state[4]),
			'fruit_right': int(state[5]),
			'fruit_down': int(state[6]),
			'direction': int(state[7]),
			'action': [straight, left, right]
		}
		self.q_table['state'].append(item)
		return item

	# Get a raw from the Q-Table
	def getItem(self, state):
		qItem = None
		for item in self.q_table['state']:
			if item['danger_straight'] == state[0]:
				if item['danger_left'] == state[1]:
					if item['danger_right'] == state[2]:
						if item['fruit_up'] == state[3]:
							if item['fruit_left'] == state[4]:
								if item['fruit_right'] == state[5]:
									if item['fruit_down'] == state[6]:
										if item['direction'] == state[7]:
											qItem = item
		# If the raw does not exist, create a new one
		if qItem == None:
			qItem = self.addNewItem(state, 0, 0, 0)
		return qItem