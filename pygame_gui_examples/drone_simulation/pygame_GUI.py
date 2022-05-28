import pygame
import random
import time
import numpy

pygame.init()




position_where = [(1,0), (0,1), (-1,0), (0,-1)]
b = random.choice(position_where)

c = random.randrange(1,30)

x = random.randint(60,700)
y = random.randint(60,700)




SCREEN_WIDTH = 850
SCREEN_HEIGHT  = 751
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Simulation")
background = pygame.image.load("C:/Users/hyeje/Desktop/pythonworkspace/rsc/images/MAP.png")


    
drone = pygame.image.load('C:/Users/hyeje/Desktop/pythonworkspace/rsc/images/drone3.png')
#position = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT - SCREEN_HEIGHT/4)
#direction = pygame.math.Vector2(0, -1)
position = pygame.math.Vector2(x,y)
direction = pygame.math.Vector2(0,1)
drone_Rect = drone.get_rect()
run = True
drone_Rect.centerx = round(SCREEN_WIDTH / 2)
drone_Rect.centery = round(SCREEN_HEIGHT / 2)

def wrap_around_screen():
    if position.x > SCREEN_WIDTH:
        position.x = 0
    if position.x < 0:
       position.x = SCREEN_WIDTH
    if position.y <= 0:
        position.y = SCREEN_HEIGHT
    if position.y > SCREEN_HEIGHT:
        position.y = 0
        
while run:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    '''position += direction        
    keys = pygame.key.get_pressed()  
    if keys[pygame.K_d]:
        direction.rotate_ip(1)
    if keys[pygame.K_a]:
        direction.rotate_ip(-1)'''

            
    direction_where = ['go', 'left', 'right']
    a = random.choice(direction_where)
    
    if a == 'go':
        for i in range(0,2):
            position += direction
            pygame.display.flip()
    
    if a == 'left':

        for i in range(0,15):
            direction.rotate_ip(-1)
            position += direction
            pygame.display.flip()

        
    if a == 'right':
        for i in range(0,15):
            direction.rotate_ip(1)
            position += direction
            pygame.display.flip()

                
    
    wrap_around_screen()

    window.fill(0)
    window.blit(background, (0, 0))
    angle = direction.angle_to((1, 0))
    rotated_drone = pygame.transform.rotate(drone, angle)
    window.blit(rotated_drone, rotated_drone.get_rect(center = (round(position.x), round(position.y))))

    pygame.display.flip()


pygame.quit()
exit()
