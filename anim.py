import sys
import random

import pygame
from pygame.locals import DOUBLEBUF, KEYDOWN, KEYUP, K_ESCAPE, FULLSCREEN, K_SPACE

screen = pygame.display.set_mode((640, 480), DOUBLEBUF) # 
clock = pygame.time.Clock() 

# Resources
# http://thelycaeum.in/resources/enemy.png
# http://thelycaeum.in/resources/enemy-small.png
# http://thelycaeum.in/resources/ship.png
# http://thelycaeum.in/resources/laser.png
# http://thelycaeum.in/resources/explosion_strip16.png

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super (Explosion, self).__init__()
        self.add(group)
        sheet = pygame.image.load("explosion_strip16.png").convert_alpha()
        self.images = []
        self.index = 0
        for i in range(0, 1536, 96):
            img = pygame.Surface((96, 96), pygame.SRCALPHA).convert_alpha()
            img.blit(sheet, dest=(0,0), area = (i, 0, i+96, 96))
            self.images.append(img)
        self.image = self.images[-1]
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.delay = random.randint(1, 15)
    
    def update(self):
        self.delay -=1
        if self.delay <= 0:
            self.image = self.images[self.index]
            self.index += 1
            self.index %= len(self.images)
            if self.index == 0:
                self.kill()
            
        
        
        

class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super (EnemyLaser, self).__init__()
        self.add(group)
        sheet = pygame.image.load("laser.png").convert_alpha()
        self.image = pygame.Surface((128, 32), pygame.SRCALPHA).convert_alpha()
        self.image.blit(sheet, dest=(0,0), area=(0,0,128,32))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        x, y = self.rect.center
        x += 50
        if x > 640:
            self.kill()
        self.rect.center = x, y


class FighterLaser(pygame.sprite.Sprite):
    def __init__(self, x, y, group):
        super (FighterLaser, self).__init__()
        self.add(group)
        sheet = pygame.image.load("hero-laser.png").convert_alpha()
        self.image = pygame.Surface((64, 16), pygame.SRCALPHA).convert_alpha()
        self.image.blit(sheet, dest=(0,0), area=(0,0,64,16))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        x, y = self.rect.center
        x -= 75
        if x < 0:
            self.kill()
        self.rect.center = x, y



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, fighter, group, fire_group):
        super(Enemy, self).__init__()
        self.good = pygame.image.load("enemy-small.png").convert_alpha()
        self.hit = pygame.image.load("enemy-hit.png").convert_alpha()
        self.image = self.good
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.add(group)
        self.fighter = fighter
        self.velocity = 0
        self.main_laser_counter = 0
        self.fire_group = fire_group
        self.laser = False 
        self.impacted = False
        self.energy = 200
        self.main_group = group

    def impact(self):
        self.impacted = True
        self.energy -= 10

    def update(self):
        f_x, f_y = self.fighter.rect.center
        s_x, s_y = self.rect.center
        if self.energy < 0:
            self.kill()
            x0,y0 = self.rect.topleft
            x1,y1 = self.rect.bottomright
            x0 -= 10
            y0 -= 10
            x1 += 10
            y1 += 10
            for i in range(25):
                Explosion(random.randint(x0,x1), random.randint(y0,y1), self.main_group)
        if s_y > f_y:
            self.velocity = -1
            self.main_laser_counter = 0
        elif s_y < f_y:
            self.velocity = 1
            self.main_laser_counter = 0
        else:
            self.velocity = 0 
            if self.main_laser_counter != 30:
                self.main_laser_counter += 1

        if not (self.laser and self.laser.alive()):
            if self.main_laser_counter == 30:
                self.laser = EnemyLaser(s_x, s_y, self.fire_group)

        if self.impacted: # If hit
            self.image = self.hit # Make the ship white for a frame
            self.impacted = False # Then mark it as not being hit
        else:
            self.image = self.good # Regular good ship

            

        s_y += self.velocity
        self.rect.center = s_x, s_y
            
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, group, fire_group):
        super(Ship, self).__init__()
        self.good = pygame.image.load("ship.png").convert_alpha()
        self.hit = pygame.image.load("ship-hit.png").convert_alpha()
        self.image = self.good
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.add(group)
        self.impacted = False
        self.energy = 100
        self.groups = group
        self.fire = False
        self.laser = False
        self.fire_group = fire_group
    
    def impact(self):
        self.impacted = True
        self.energy -= 10

    def update(self):
        x, y = pygame.mouse.get_pos()
        self.rect.center = (x,y)
        if self.fire:
            self.laser = FighterLaser(x, y, self.fire_group)
                            
        if self.energy < 0:
            self.kill()
            x0,y0 = self.rect.topleft
            x1,y1 = self.rect.bottomright
            x0 -= 10
            y0 -= 10
            x1 += 10
            y1 += 10
            for i in range(10):
                Explosion(random.randint(x0,x1), random.randint(y0,y1), self.groups)
        if self.impacted: # If hit
            self.image = self.hit # Make the ship white for a frame
            self.impacted = False # Then mark it as not being hit
        else:
            self.image = self.good # Regular good ship

class MySprite(pygame.sprite.Sprite):
    def __init__(self, x, y, vel, col, group):
        super(MySprite, self).__init__()
        self.image = pygame.Surface((3, 3))
        self.image.fill((col, col, col))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.add(group)
        self.vel = vel

    def update(self):
        x,y = self.rect.center
        if x > 640 :
            x = 0
        x += self.vel
        self.rect.center = x,y


all_sprites = pygame.sprite.Group()
enemy_fire = pygame.sprite.Group()
ship_fire = pygame.sprite.Group()
background = pygame.Surface((640, 480))

for i in range(100):
    x = random.randint(0, 640)
    y = random.randint(0, 480)
    MySprite(x, y, 5, 100, all_sprites)
for i in range(50):
    x = random.randint(0, 640)
    y = random.randint(0, 480)
    MySprite(x, y, 15, 150, all_sprites)
for i in range(25):
    x = random.randint(0, 640)
    y = random.randint(0, 480)
    MySprite(x, y, 25, 200, all_sprites)

fighter = Ship(320, 240, all_sprites, [all_sprites,ship_fire]) # Create a ship
enemy = Enemy(200, 240, fighter, all_sprites, [all_sprites, enemy_fire]) # Create an enemy ship (pass the fighter to it)

pygame.mouse.set_visible(False)

while True:
    clock.tick(20)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print ("Thanks for playing!")
                sys.exit(0)
            if event.key == K_SPACE:
                fighter.fire = True
        elif event.type == KEYUP:
            if event.key == K_SPACE:
                fighter.fire = False            

    
    collided = pygame.sprite.spritecollideany(fighter, enemy_fire)
    # http://thelycaeum.in/resources/ship-hit.png
    if collided:
        collided.kill()
        fighter.impact()

    collided = pygame.sprite.spritecollideany(enemy, ship_fire)
    if collided:
        collided.kill()
        enemy.impact()
    
        
            
    all_sprites.clear(screen, background)
    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()                



raw_input()




