# Thread the Needle - a pyGame program by Griffin Withington
import pygame
pygame.init()
from random import seed
from random import randint
from math import sqrt

# SETUP
#########################
displaywidth = 800                                                              # Sets display width in pixels
displayheight = 600                                                             # Sets display height in pixels
win = pygame.display.set_mode((displaywidth, displayheight))                    # Opens window for game display and names window "win"

pygame.display.set_caption("Thread The Needle")                                 # Captions game with title "Thread the Needle"
clock = pygame.time.Clock()                                                     # Necessary to institute fps frame change
fps = 60                                                                        # Sets frame rate at 60 frames per second
#########################



# SPRITES
#########################
cansprite = pygame.image.load('lasercannon.png')                                # Loads in laser cannon sprite to be implemented
cansize = 70                                                                    # Sets pixel side-length of square cannon sprite
canspritescale = pygame.transform.scale(cansprite, (cansize, cansize))          # Scales laser cannon sprite to cansize

frsprite = pygame.image.load('downfreighter.png')                               # Same as above for freighter sprite
frheight = 50
frspritescale = pygame.transform.scale(frsprite, (int((95/151)*frheight), frheight))

#########################



# CANNON class
########################

class cannon(object):
    def __init__(self, x, y, width, height, cooldown, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cooldown = cooldown
        self.timer = 0
        self.speed = speed
        self.scope = False
        self.hit = False
        self.hittimer = 0

    def draw(self, win):
#        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)
        win.blit(canspritescale, (self.x, self.y))

    def drawcooldown(self, win):
        pygame.draw.rect(win, (255, 0, 255), (self.x - 18, self.y, 10, self.height))
        pygame.draw.rect(win, (0, 0, 0), (self.x - 18, self.y, 10, int(self.height * self.timer/(self.cooldown * fps))))


    def drawhit(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height), 50)


    def drawscope(self, win):
        for i in range(1, 12):
            pygame.draw.rect(win, (112,128,144), (self.x + 60*i + 20, self.y + int((self.height / 2) - 1), 35, 1), 2)


########################



# LASER class
########################

class laser(object):
    def __init__(self, speed, color, x, y, width, height, angle):
        self.speed = speed
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))



# PAYLOAD class
#############################
class payload(object):
    def __init__(self, radius, x, y):
        self.radius = radius
        self.color = (0, 200, 0)
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)





# BOMB class
#########################
class bomb(object):
    def __init__(self, radius, x, y, speed):
        self.radius = radius
        self.color = (255, 0, 0)
        self.x = x
        self.y = y
        self.speed = speed

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


# FREIGHTER class
############################
class freighter(object):
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def draw(self, win):
    #    pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        win.blit(frspritescale, (self.x, self.y))



# LEVEL CLASS
#########################
class level(object):                                                            # LEVEL CLASS used to incrementally increase difficulty of game
    def __init__(self, level):                                                  # by tweaking perameters when score reaches new benchmarks
        self.level = 1
                                                                                # To be written later






# UPDATING GAME WINDOW
#########################
def redrawGameWindow():                                                         # Redraws the game window for each frame, thus it runs 60 times/second
                                                                                # Function will be called at the end of the game-run while loop
    win.fill((0,0,0))
    can.draw(win)
    can.drawcooldown(win)                                                       # The function operates simply, redrawing all active game elements in their new location
    load.draw(win)
    for las in lasers:
        las.draw(win)
    for fr in freighters:
        fr.draw(win)
    for b in bombs:
        b.draw(win)
    if can.scope:
        can.drawscope(win)
    if can.hit:
        can.drawhit(win)
    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (150, 480))
    pygame.display.update()




# GAMERUN
########################

font = pygame.font.SysFont('comicsans', 35, True)
can = cannon(50, 270, cansize, cansize, 1, 4)                                   # instance of laser cannon location (50, 270), preset cannon size, 1 second cooldown, movement speed 4
load = payload(40, 720, 300)                                                    # instance of payload location (720, 300), radius of 10 pixels

lasers = []
freighters = []
freightercooldown = 0
bombs = []
bombcooldown = 0
score = 0


run = True                                                                      # Setting run to True allows the following while loop to run indefinitely
while run:                                                                      # Creates a while loop to run for the entirity of the game


    clock.tick(fps)                                                             # game set to FPS set above
    for event in pygame.event.get():                                            # Allowing for computer interaction
        if event.type == pygame.QUIT:                                           # during gameplay
            run = False                                                         # Stops the running of the game in the event of closing out of the game window

# COOLDOWN UPDATES
    if can.timer > 0:
        can.timer -= 1
    if can.hittimer > 0:
        can.hittimer -= 1
    if can.hittimer == 0:
        can.hit = False

    keys = pygame.key.get_pressed()

# CANON MOVEMENT
    if keys[pygame.K_e] and keys[pygame.K_c]:
        pass
    elif keys[pygame.K_e] and can.y > 0:
        can.y -= can.speed
    elif keys[pygame.K_c] and can.y < 600:
        can.y += can.speed

# LASER SCOPE
    can.scope = False
    if keys[pygame.K_f]:
        can.scope = True


# LASER FIRING
    if keys[pygame.K_SPACE] and can.timer == 0 and can.hittimer == 0:
        lasers.append(laser(50, (255, 0, 255), can.x + can.width - 50, can.y + (int(can.height / 2)), 50, 3, 0))   # laser args: (speed, color, x, y, width, height, angle)
        can.timer = can.cooldown * fps

# LASER MOVEMENT
    for las in lasers:
        if las.x < 800:
            las.x += las.speed
        else:
            lasers.pop(lasers.index(las))

# LASER COLLISION
#    for las in laser:
#        for fr in freighters:
#            if las.x +


# FREIGHTER GENERATION
    freightgen = randint(1, 15)
    if freightercooldown == 0 and freightgen == 1:
        freighters.append(freighter(600, -70, int(8*50/frheight), frheight, (255,255,255), 3))         # freighter args: (x, y, width, height, color, speed)
        freightercooldown = 17
    if freightercooldown > 0:
        freightercooldown -= 1

# FREIGHTER MOVEMENT
    for fr in freighters:
        if fr.y < 600:
            fr.y += fr.speed
        else:
            freighters.pop(freighters.index(fr))

# BOMB GENERATION
    bombgen = randint(1, 50)
    if bombcooldown == 0 and bombgen == 1:
        bombx = randint(640, 800)
        bombs.append(bomb(10, bombx, 0, 1))
        bombcooldown = 55
    if bombcooldown > 0:
        bombcooldown -= 1

# BOMB MOVEMENT
    for b in bombs:
        if b.y < 600:
            b.y += b.speed
        else:
            bombs.pop(bombs.index(b))


# BOMB LANDING ON PAYLOAD
    for b in bombs:
        if b.x >= load.x - load.radius - b.radius and b.x <= load.x + load.radius + b.radius:
            if b.y >= load.y - sqrt(((load.radius + b.radius) ** 2 - ((load.x - b.x) ** 2))):
                bombs.pop(bombs.index(b))
                if load.radius > 2:
                    load.radius -= 2

# LASER HITTING BOMB
    for las in lasers:
        for fr in freighters:
            if las.y >= fr.y and las.y + las.height <= fr.y + fr.height and las.x >= fr.x - las.speed and las.x <= fr.x:
                freighters.pop(freighters.index(fr))
                las.speed = -1 * las.speed

# LASER HITTING CANNON
    for las in lasers:
        if las.y >= can.y and las.y + las.height <= can.y + can.height and las.x <= can.x and las.x >= can.x + las.speed and las.speed < 0:
            lasers.pop(lasers.index(las))
            can.hit = True
            can.hittimer = 90

# LASER HITTING BOMB
    for las in lasers:
        for b in bombs:
            if las.y >= b.y - b.radius and las.y +las.height <= b.y + b.radius and las.x + las.width <= b.x and las.x + las.width >= b.x - las.speed:
                bombs.pop(bombs.index(b))
                lasers.pop(lasers.index(las))
                score += 1




    redrawGameWindow()                                                          # Redraws game state - occurs 27 times/second










########################


pygame.quit()


# SPRITE URLS FOR CITATION
############################
# http://millionthvector.blogspot.com/p/free-sprites.html
# http://millionthvector.blogspot.com/p/free-sprites.html





'''
to do list:

1. bullet cooldown and visual (declining bar)
2.
'''
