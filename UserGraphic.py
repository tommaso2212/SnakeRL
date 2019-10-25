###
# This class is used to draw an user interface for the game
###

import pygame
import time
from Parameters import Parameters as par

class UserGraphic:

	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode([par.PLAYGROUND_WIDTH*20, par.PLAYGROUND_HEIGHT*20])

	def draw(self, playground):
		self.window.fill((255, 255, 255))
		for i in range(0, par.PLAYGROUND_WIDTH):
			for j in range(0, par.PLAYGROUND_HEIGHT):
				self.drawItem(playground[i, j], i, j)
		pygame.display.flip()
		#time.sleep(0.5)

	def drawItem(self, obj, x, y):
		if obj == par.OBJ_FRUIT:
			pygame.draw.rect(self.window, (255, 0, 0), (x*20, y*20, 20, 20))
		elif obj == par.OBJ_HEAD:
			pygame.draw.rect(self.window, (0, 0, 255), (x*20, y*20, 20, 20))
		elif obj == par.OBJ_BODY or obj == par.OBJ_TAIL:
			pygame.draw.rect(self.window, (0, 255, 0), (x*20, y*20, 20, 20))
		else:
			pygame.draw.rect(self.window, (255, 255, 255), (x*20, y*20, 20, 20))

	def close(self):
		pygame.quit()