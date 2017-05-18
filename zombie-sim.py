#===============================================================================
#                            General Documentation
#
"""This is the long description of the zombie simulation
"""

#-------------------------------------------------------------------------------
#                           Additional Documentation
#
#   Authors:    Destiny Boyer, Taran Christensen, Scott Feurguson, Jeremy Luxom
#   Date:       5/1/2017
#   Class:      CSS 458 - Computer Simulation
#   Assignment: Final Project, Zombie Simulation
#===============================================================================

#-------------------- Module General Import and Declarations -------------------
import numpy as np
import matplotlib.pyplot as plt
from humans import Human
from zombie import Zombie

#---------------------------- User defined variables ---------------------------
visual = True
runs = 1                # times to run the sim
pop_human = 40          # initial population of humans
pop_zombie = 12         # initial population of zombies
water_stores = 6        # number of water locations
speed_human = .0035     # speed of humans
speed_zombie = .004     # speed of zombies
human_spread = .0007    # spread of human speed
zombie_spread = .0005   # variance in speed of humans/zombies
zombie_life = 200       # zombie lifetime
zombie_range = .35      # zombie range of sight
radius = .01

#------------------------------ Constant variables -----------------------------
color_human = (0., .9, 0.)
color_zombie = (.9, 0., 0.)
color_water = (0., 0., .9)

# used in the main loop
two_radius_sq = (radius * 2) ** 2
zombie_range_sq = zombie_range ** 2

# edges of the square, with radius offset
left = .4 - radius
right = .6 + radius
top = .6 + radius
bottom = .4 - radius

#------------------------------- Global variables ------------------------------
# global to stop the main loop if needed
go = True
humans = []
zombies = []
water = []
infected = []
decayed = []

#-------------------------------- Helper Methods -------------------------------
# listener for key press events
def on_key_press(event):
    global go
    if event.key == ' ': # if space is pressed, stop the sim
        go = False

# generate a new random circle starting position
def newPos():
    while True:
        pos = np.random.random(2)
        if pos[0] < bottom or pos[0] > top or pos[1] < left or pos[1] > right:
            return pos

def wrapDiff(diff):
    diff = np.where(diff > 0.5, -1. + diff, diff)
    return np.where(diff < -0.5, 1. + diff, diff)

def collisionOffset(start, lead, target, mag):
    ratio = lead / mag
    if target < 0:
        mag = -mag
    return (start + target * ratio + (1. - ratio) * mag) % 1.

def move(agent, vec, mag):
    y = (agent.plot.center[0] + vec[0]) % 1.
    x = (agent.plot.center[1] + vec[1]) % 1.
    if not (y < bottom or y > top or x < left or x > right):
        ydiff = y - .5
        xdiff = x - .5
        if ydiff < xdiff:
            if ydiff < -xdiff:
                x = collisionOffset(agent.plot.center[1], bottom - agent.plot.center[0], vec[1], mag)
                y = bottom
            else:
                y = collisionOffset(agent.plot.center[0], agent.plot.center[1] - right, vec[0], mag)
                x = right
        else:
            if ydiff < -xdiff:
                y = collisionOffset(agent.plot.center[0], left - agent.plot.center[1], vec[0], mag)
                x = left
            else:
                x = collisionOffset(agent.plot.center[1], agent.plot.center[0] - top, vec[1], mag)
                y = top
    agent.plot.center = (y, x)
    
def calculateSpeed(speed, spread):
    return np.random.normal(speed, spread)

def initializePopulations():
    for i in range(pop_human):
        speed = calculateSpeed(speed_human, human_spread)
        human = Human(speed)
        human.plot = plt.Circle(newPos(), radius, color=color_human)
        humans.append(human)
        if visual:
            ax.add_artist(human.plot)
    for i in range(pop_zombie):
        speed = calculateSpeed(speed_zombie, zombie_spread)
        zombie = Zombie(speed)
        zombie.plot = plt.Circle(newPos(), radius, color=color_zombie)
        zombies.append(zombie)
        if visual:
            ax.add_artist(zombie.plot)
    for i in range(water_stores):
        c = plt.Circle(newPos(), radius, color=color_water)
        water.append(c)
        if visual:
            ax.add_artist(c)

def moveZombies():
    global decayed
    decayed = []
    
    humanCenters = np.array([human.plot.center for human in humans])
    for zombie in zombies:
        zombie = zombie.decay()
        if zombie.time_till_death == 0:
            decayed.append(zombie)
        dist = zombie_range_sq
        vec = (0., 0.)
        
        ydiff = wrapDiff(humanCenters[:,0] - zombie.plot.center[0]) # Flipped?
        xdiff = wrapDiff(humanCenters[:,1] - zombie.plot.center[1])
        sqdist = ydiff ** 2 + xdiff ** 2
        minDistIdx = np.argmin(sqdist)
        if sqdist[minDistIdx] < dist:
            dist = sqdist[minDistIdx]
            vec = (ydiff[minDistIdx], xdiff[minDistIdx])
            
        """ Old Non-Array Code
        for human in humans:
            ydiff = wrapDiff(human.center[0] - zombie.center[0])
            xdiff = wrapDiff(human.center[1] - zombie.center[1])
            sqdist = ydiff ** 2 + xdiff ** 2
            if sqdist < dist:
                dist = sqdist
                vec = (ydiff, xdiff)
        """
        dist = np.sqrt(dist) / zombie.speed
        move(zombie, (vec[0] / dist, vec[1] / dist), zombie.speed)

def cleanupZombies():
    for zombie in decayed:
        zombies.remove(zombie)
        if visual:
            zombie.remove()

def moveAndInfectHumans():
    global infected
    infected = []
    
    zombieCenters = np.array([zombie.plot.center for zombie in zombies])
    for human in humans:
        vec = (0., 0.)
        
        ydiff = wrapDiff(human.plot.center[0] - zombieCenters[:,0]) # Flipped?
        xdiff = wrapDiff(human.plot.center[1] - zombieCenters[:,1])
        sqdist = ydiff ** 2 + xdiff ** 2
        minDistIdx = np.argmin(sqdist)
        if sqdist[minDistIdx] < two_radius_sq:
            infected.append(human)
            continue
            
        vec = (np.sum(ydiff/sqdist), np.sum(xdiff/sqdist))
        
        """ Old Non-Array Code
        for zombie in zombies:
            ydiff = wrapDiff(human.center[0] - zombie.center[0])
            xdiff = wrapDiff(human.center[1] - zombie.center[1])
            sqdist = ydiff ** 2 + xdiff ** 2
            vec = (vec[0] + ydiff / sqdist, vec[1] + xdiff / sqdist)
            if sqdist < two_radius_sq:
                infected.append(human)
                break
        """
        mag = np.sqrt(vec[0] ** 2 + vec[1] ** 2) / human.speed
        move(human, (vec[0] / mag, vec[1] / mag), human.speed)

def zombifyInfected():
    for human in infected:
        humans.remove(human)
        speed = calculateSpeed(speed_zombie, zombie_spread)
        zombie = Zombie(speed)
        zombie.plot = plt.Circle(newPos(), radius, color=color_zombie)
        zombies.append(zombie)

#--------------------------------- Main Methods --------------------------------
if __name__ == "__main__":
    if visual:
        # create the figure
        fig = plt.figure(num=1, figsize=(10, 8))
        fig.canvas.mpl_connect('key_press_event', on_key_press)
        
        # create the main axes
        ax = fig.add_axes((0., 0., .8, 1.))
        # todo: add some stats on the side
        
        # create square wall in the middle
        # todo: use more complex walls
        rect = plt.Rectangle((.4, .4), .2, .2, color=(.5, .5, .5))
        ax.add_artist(rect)
        
        plt.show()
    # main simulation loop
    for i in range(runs):
        
        # create the human and zombie circles
        initializePopulations()

        while go:
            # Move every zombie to the human that is the closest
            moveZombies() 
                
            # Clean up any decayed zombies from the simulation
            cleanupZombies()
            
            if len(zombies) != 0:
                # For every human in the simulation, run away from any zombies 
                #  nearby, and if there is a zombie near enough then this human 
                #  is infected
                moveAndInfectHumans()
                    
                # Turn infected humans into zombies
                zombifyInfected()
                    
            # If we're plotting the simulation, wait a milisecond (why?) then
            #  draw the simulation
            if visual:
                plt.pause(.001)
                plt.draw()
                
            # Finish when either humans or zombies "win"
            if len(humans) == 0 or len(zombies) == 0:
                break
        
        #print 'humans: ' + str(len(humans)) + ' zombies: ' + str(len(zombies))
        if not go:
            break
    
