import sys

import pygame
from pygame.locals import DOUBLEBUF, KEYDOWN, K_ESCAPE, K_a, K_s, K_d

screen = pygame.display.set_mode((640, 480), DOUBLEBUF) # 


clock = pygame.time.Clock() 

colour = "blue"

while True:
    for i in range(255):  
        clock.tick(200)
        if colour == "red":
            screen.fill((i, 0, 0))
        elif colour == "green":
            screen.fill((0, i, 0))
        elif colour == "blue":
            screen.fill((0, 0, i))
        
        pygame.display.flip()
 
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    print ("Thanks for playing!")
                    sys.exit(0)
                if event.key == K_a:
                    colour = "red"
                if event.key == K_s:
                    colour = "blue"
                if event.key == K_d:
                    colour = "green"

                



raw_input()




