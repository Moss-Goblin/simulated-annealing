import pygame
import math
import random

# smaller score = better
def getScore(color_r, color_g, color_b):
    return color_r + color_g + color_b

# to do - redo this neighbor choosing algorithm to prefer similar value neighbors
def randMove(cur_x, cur_y, max_x, max_y):
    next_x = min(max(cur_x + random.randint(-1,1), 0), max_x)
    next_y = min(max(cur_y + random.randint(-1,1), 0), max_y)
    return next_x, next_y

# acceptance probability function
# higher number returned = higher chance
def P(old_score, new_score, cur_temp):
    to_return = old_score - new_score
    #to_return = math.pow(to_return,3)
    if cur_temp > 0:
        to_return += math.log10(cur_temp)*10

    if cur_temp < 100:
        print(str(to_return))
    return math.floor(to_return)

# number of millisecs for each step
refresh_rate = 1

# number of steps to run the algorithm for (plus ~1k at the end)
cur_temp = 100000

pygame.init()
screen_width = 600
screen_height = 600

# create canvas
scrn = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('image')
imp = pygame.image.load("circles.png").convert()

screen_width = imp.get_width()
screen_height = imp.get_height()

scrn = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Using blit to copy content from one surface to other
scrn.blit(imp, (0, 0))

# paint screen one time
pygame.display.flip()

# starting position - just choosing the middle atm
cur_x = math.floor(screen_width/2)
cur_y = math.floor(screen_height/2)
# arbitrary high score so it'll choose the next position
cur_score = 800

status = True
while (status):
    pygame.time.wait(refresh_rate)

    # reset image to base
    scrn.blit(imp, (0, 0))
    # draw a plus at the current position
    scrn.set_at([cur_x, cur_y], [255, 100, 100])
    scrn.set_at([max(cur_x-1,0), cur_y], [255, 100, 100])
    scrn.set_at([min(cur_x+1,screen_width), cur_y], [255, 100, 100])
    scrn.set_at([cur_x, max(cur_y-1,0)], [255, 100, 100])
    scrn.set_at([cur_x, min(cur_y+1,screen_height)], [255, 100, 100])
    pygame.display.flip()

    # progress printout
    if cur_temp%1000 == 0:
        print(str(math.floor(cur_temp/1000)))
    #print(str(cur_x) + "," + str(cur_y))

    if (cur_temp > -1000):
        next_x, next_y = randMove(cur_x,cur_y,screen_width,screen_height)
        next_color = scrn.get_at([next_x, next_y])
        next_score = getScore(next_color.r,next_color.g,next_color.b)
        chance = P(cur_score,next_score,cur_temp)
        if chance > random.randint(0,100):
            cur_x = next_x
            cur_y = next_y
            cur_score = next_score
        #print("Chance: " + str(chance))

    cur_temp -= 1

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for i in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if i.type == pygame.QUIT:
            status = False

# deactivates the pygame library
pygame.quit()
