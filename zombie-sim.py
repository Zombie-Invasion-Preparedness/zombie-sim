#===============================================================================
#                            General Documentation
#
"""This is the long description of the zombie simulation
"""

#-------------------------------------------------------------------------------
#                           Additional Documentation
#
#   Authors:    Destiny Boyer, Taran Christensen, Scott Ferguson, Jeremy Luxon
#   Date:       5/1/2017
#   Class:      CSS 458 - Computer Simulation
#   Assignment: Final Project, Zombie Simulation
#===============================================================================

#-------------------- Module General Import and Declarations -------------------
import numpy as np
from humans import Human
from zombie import Zombie
import pygame

#---------------------------- User defined variables ---------------------------
visual = True
runs = 1                # times to run the sim
pop_human = 100         # initial population of humans
pop_zombie = 12         # initial population of zombies
water_stores = 6        # number of water locations
speed_human = 1.75      # speed of humans
speed_zombie = 2.       # speed of zombies
human_spread = .35      # spread of human speed
zombie_spread = .25     # variance in speed of humans/zombies
zombie_life = 200       # zombie lifetime
zombie_range = 175      # zombie range of sight
radius = 5

#------------------------------ Constant variables -----------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# used in the main loop
two_radius_sq = (radius * 2) ** 2
zombie_range_sq = zombie_range ** 2

# screen dimensions
WIDTH = 1024
HEIGHT = 512

# edges of the square, with radius offset
left = 0. - radius
right = WIDTH + radius
top = 0.0 + radius
bottom = HEIGHT - radius

#------------------------------- Global variables ------------------------------
list_humans = []	# holds the human objects
list_zombies = []	# holds the zombie objects
list_water = []		# holds water objects
list_food = []		# holds food objects

water = []
infected = []
decayed = []

#-------------------------------- Helper Methods -------------------------------

def newPos():
    """ Genereate a new random starting position for an agent

    Output:
    * A two element array consisting of two random floats that are inside the 
    bounaries of the play area defined by 'left', 'right', 'bottom', and 'top'. 
    """
    while True:
        pos = np.random.random(2) * (HEIGHT, WIDTH)
        if pos[0] < bottom or pos[0] > top or pos[1] < left or pos[1] > right:
            return pos

def wrapDiffX(diff):
    """ Function to wrap the difference between two positions

    Method Arguments:
    * diff: Computed difference of distance between two agents 

    Output:
    * An integer corresponding to the difference between two agents, properly
    wrapped. Values that are properly wrapped have been put between -0.5 and 0.5
    """
    diff = np.where(diff > WIDTH/2, -WIDTH + diff, diff)
    return np.where(diff < -WIDTH/2., WIDTH + diff, diff)

def wrapDiffY(diff):
    """ Function to wrap the difference between two positions

    Method Arguments:
    * diff: Computed difference of distance between two agents 

    Output:
    * An integer corresponding to the difference between two agents, properly
    wrapped. Values that are properly wrapped have been put between -0.5 and 0.5
    """
    diff = np.where(diff > HEIGHT/2, -HEIGHT + diff, diff)
    return np.where(diff < -HEIGHT/2, HEIGHT + diff, diff)

def collisionOffset(start, lead, target, mag):
    """Docstring

    Method Arguments:
    * start: 
    * lead:
    * target:
    * mag:

    Output:
    * Output vals
    """
    ratio = lead / mag
    if target < 0:
        mag = -mag
    return (start + target * ratio + (1. - ratio) * mag) % 1.

def move(circle, vec, mag):
    """Function to handle the movement of agents around the canvas

    Method Arguments:
    * agent: The zombie/human agent that will be updated and moved
    * vec:
    * mag:

    Output:
    * An updated x, y location for the agent based on set conditions
    """
    y = (circle.y + vec[0]) % HEIGHT
    x = (circle.x + vec[1]) % WIDTH
    if not (y < bottom or y > top or x < left or x > right):
        ydiff = y - HEIGHT/2.
        xdiff = x - WIDTH/2.
        if ydiff < xdiff:
            if ydiff < -xdiff:
                x = collisionOffset(circle.x, bottom - circle.y , vec[1], mag)
                y = bottom
            else:
                y = collisionOffset(circle.y ,circle.x - right, vec[0], mag)
                x = right
        else:
            if ydiff < -xdiff:
                y = collisionOffset(circle.y , left - circle.x, vec[0], mag)
                x = left
            else:
                x = collisionOffset(circle.x, circle.y  - top, vec[1], mag)
                y = top

    circle.y = y
    circle.x = x

def calculateSpeed(speed, spread):
    """Calculate the speed of the agent using a normal 
    distribution between two values

    Method Arguments:
    * speed: The speed of the agent. This value is predefined
    and is different for the zombie and human agents
    * spread: The possible spread for the values of speed. This 
    value is predefined and is different for the zombie and human agents.


    Output:
    * An integer value corresponding to the speed of the agent
    """
    return np.random.normal(speed, spread)

def initializePopulations():
    """A function that initializes all agents

    Output:
    * Each class will have a number of agents from a predefined 
    variable, and will be added into the simulation
    """
    for i in range(pop_human):
        speed = calculateSpeed(speed_human, human_spread)
        y, x = newPos()
        human = Human(speed, GREEN, x, y)
        list_humans.append(human)

    for i in range(pop_zombie):
        speed = calculateSpeed(speed_zombie, zombie_spread)
        y, x = newPos()
        zombie = Zombie(speed, RED, x, y)
        list_zombies.append(zombie)

def zombifyInfected():
    """A method to handle the human agents that have been
    infected and will turn them into zombie agents

    Output:
    * An updated zombie list that now includes previously infected humans
    """
    for human in infected:
        list_humans.remove(human)
        human.speed = np.random.normal(speed_zombie, zombie_spread) # new speed
        zombie = Zombie(human.speed, RED, human.x, human.y) # make a new zombie agent at the human's location
        zombie.set_time_till_death() # set the new time of death
        list_zombies.append(zombie)

def cleanupZombies():
    """Helper function to handle the zombie agents that have reached
    their time limit and need to be removed

    Output:
    * an updated list of zombies, and the removal of the decayed zombie agents
    from the canvas
    """
    global decayed

    for zombie in decayed:
        list_zombies.remove(zombie)

def moveZombies():
    """Function to handle the movement of zombie agents around
    the canvas and to properly decay the zombie agents. Zombie agents attempt to 
    reach the closest human in their range of sight

    Output:
    * Calls the move() function for the zombie agent
    """
    global decayed
    decayed = []

    humanCenters = np.array([human.pos() for human in list_humans])
    for zombie in list_zombies:
        zombie.decay()  # decay
        if zombie.time_till_death < 0: # cant use == 0
            decayed.append(zombie)
        dist = zombie_range_sq  # zombie range of sight ** 2
        vec = (0., 0.)

        # distances between the humans and zombie agents
        ydiff = wrapDiffY(humanCenters[:, 0] - zombie.y)  # Flipped?
        xdiff = wrapDiffX(humanCenters[:, 1] - zombie.x)
        sqdist = ydiff ** 2 + xdiff ** 2
        minDistIdx = np.argmin(sqdist)
        if sqdist[minDistIdx] < dist:
            dist = sqdist[minDistIdx]
            vec = (ydiff[minDistIdx], xdiff[minDistIdx])

        dist = np.sqrt(dist) / zombie.speed
        move(zombie, (vec[0] / dist, vec[1] / dist), zombie.speed)

def moveAndInfectHumans():
    """Function to move the human agents away from the zombie agents. If a 
    zombie agent touches a human then that human becomes infected   

    Output:
    * Calls the move() function for the human agents.
    """
    global infected
    infected = []

    zombieCenters = np.array([zombie.pos() for zombie in list_zombies])
    for human in list_humans:
        vec = (0., 0.)

        ydiff = wrapDiffY(human.y - zombieCenters[:, 0])  # Flipped?
        xdiff = wrapDiffX(human.x - zombieCenters[:, 1])
        sqdist = ydiff ** 2 + xdiff ** 2
        minDistIdx = np.argmin(sqdist)
        if sqdist[minDistIdx] < two_radius_sq:
            infected.append(human)
            continue

        vec = (np.sum(ydiff / sqdist), np.sum(xdiff / sqdist))

        mag = np.sqrt(vec[0] ** 2 + vec[1] ** 2) / human.speed
        move(human, (vec[0] / mag, vec[1] / mag), human.speed)

#--------------------------------- Main Methods --------------------------------
if __name__ == "__main__":
    done = False
    if visual:
        # Initialize pygame
        pygame.init()
        # Set the height and width of the screen
        screen_width = WIDTH
        screen_height = HEIGHT
        screen = pygame.display.set_mode((screen_width, screen_height))

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

    # main simulation loop
    for i in range(runs):

        # create the human and zombie circles
        initializePopulations()

        # handle the user clicking the x
        while not done:
            # Move every zombie to the human that is the closest
            moveZombies()

            # Clean up any decayed zombies from the simulation
            cleanupZombies()

            if len(list_zombies) != 0:
                # For every human in the simulation, run away from any zombies
                #  nearby, and if there is a zombie near enough then this human
                #  is infected
                moveAndInfectHumans()

                # Turn infected humans into zombies
                zombifyInfected()

            if visual:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                # Clear the screen
                screen.fill(WHITE)

                # Draw all the spites
                for sprite in list_humans + list_zombies:
                    pygame.draw.circle(screen, sprite.color, (int(sprite.x), int(sprite.y)), radius)
    
                # fps
                clock.tick(30)
    
                # Go ahead and update the screen with what we've drawn.
                pygame.display.update()

            # Finish when either humans or zombies "win"
            if len(list_humans) == 0 or len(list_zombies) == 0:
                break
        
        if visual:
            pygame.quit()

        print('humans: ' + str(len(list_humans)) + ' zombies: ' + str(len(list_zombies)))
        if done:
            break


