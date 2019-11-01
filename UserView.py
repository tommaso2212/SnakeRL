##
# This class is used to draw an user interface for the game
##

import pygame
import time
from Parameters import Parameters as par

class UserView:
	
	# Initialize surface
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode([par.PLAYGROUND_WIDTH*20, par.PLAYGROUND_HEIGHT*20])

	# Draw graphics
	def draw(self, playground):
		# Set background white
		self.window.fill((255, 255, 255))
		# pygame.draw.rect(self.window, (255, 255, 255), (20, 20, par.PLAYGROUND_WIDTH*20, par.PLAYGROUND_HEIGHT*20))
		# Draw each item
		for i in range(0, par.PLAYGROUND_WIDTH):
			for j in range(0, par.PLAYGROUND_HEIGHT):
				self.drawItem(playground[i, j], i, j)
        # Update display
		pygame.display.flip()
        # Delay
		#time.sleep(0.5)
	
	def drawItem(self, obj, x, y):
		if obj == par.OBJ_FRUIT:    # Draw fruit (red quad)
			pygame.draw.rect(self.window, (255, 0, 0), (x*20, y*20, 20, 20))
		elif obj == par.OBJ_HEAD:   # Draw snake's head (blue quad)
			pygame.draw.rect(self.window, (0, 0, 255), (x*20, y*20, 20, 20))
		elif obj == par.OBJ_BODY:   # Draw snake's body (green quad)
			pygame.draw.rect(self.window, (0, 255, 0), (x*20, y*20, 20, 20))
		else:   # Draw empty cell (white quad)
			pygame.draw.rect(self.window, (255, 255, 255), (x*20, y*20, 20, 20))

	# Close user view
	def close(self):
		pygame.quit()