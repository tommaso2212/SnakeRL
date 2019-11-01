##
# This class define and manage Q-Agent for the game
##

import pandas as pd
import numpy as np
from Parameters import Parameters as par
from Table import Table


class QLearning:

    def __init__(self, path=None):
        self.qTable = []
        if path:    # Load Q Table from csv file
            try:
                self.loadTable(path)
            except:
                for i in range(0, len(self.qTable)):
                    self.qTable.pop(i)
    
    def loadTable(self, path):
        dataset = pd.read_csv(path).iloc[:, 1:11].values
        for i in range(0, len(dataset)):
            self.qTable.append(Table(dataset[i, 0:6], dataset[i, 6:10]))

    def saveTable(self):
        table = pd.DataFrame(columns=['danger_upward', 'danger_left', 'danger_right', 'danger_downward', 'fruit_y', 'fruit_x', 'up_movement', 'left_movement', 'right_movement', 'down_movement'])
        with open("qTable.csv", 'w') as file:
            for row in self.qTable:
                table = table.append({'danger_upward': row.state[0], 'danger_left': row.state[1], 'danger_right': row.state[2], 'danger_downward': row.state[3], 'fruit_y': row.state[4], 'fruit_x': row.state[5], 'up_movement': row.actions[0], 'left_movement': row.actions[1], 'right_movement': row.actions[2], 'down_movement': row.actions[3]}, ignore_index=True)
            table.to_csv(file)

    def addRow(self, state):
        row = Table(state)
        self.qTable.append(row)
        return row

    # Find a row in the table
    def findState(self, state):
        for row in self.qTable:
            if np.array_equal(row.state, state):
                return row
        return self.addRow(state)

    def getAction(self, state):
        return self.findState(state).getAction()


    # Update Q-Table's value
    def updateTable(self, old_state, new_state, action, reward):
        self.findState(old_state).actions[action] = self.findState(old_state).actions[action] + par.ALPHA * (reward + par.GAMMA * np.max(self.findState(new_state).actions) - self.findState(old_state).actions[action])