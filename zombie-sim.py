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
list_humans = [] # holds the human objects
list_zombies = [] # holds the zombie objects

water = []
infected = []
decayed = []

#-------------------------------- Helper Methods -------------------------------
# listener for key press events
def on_key_press(event):
    """Listen for and handle the space bar being pressed
    
    Method Arguments:
    * event: Key pressed event object
    
    Output:
    * This method sets 'go' to false, enabling the ability to pause the active
    simulation. 'Go' is set to false when the event key corresponds to space.
    """
    global go
    if event.key == ' ': # if space is pressed, stop the sim
        go = False

def newPos():
    """ Genereate a new random starting position for an agent
    
    Output:
    * A two element array consisting of two random floats that are inside the 
    bounaries of the play area defined by 'left', 'right', 'bottom', and 'top'. 
    """
    while True:
        pos = np.random.random(2)
        if pos[0] < bottom or pos[0] > top or pos[1] < left or pos[1] > right:
            return pos

def wrapDiff(diff):
    """ Function to wrap the difference between two positions
    
    Method Arguments:
    * diff: Computed difference of distance between two agents 
    
    Output:
    * An integer corresponding to the difference between two agents, properly
    wrapped. Values that are properly wrapped have been put between -0.5 and 0.5
    """
    diff = np.where(diff > 0.5, -1. + diff, diff)
    return np.where(diff < -0.5, 1. + diff, diff)

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

def move(agent, vec, mag):
    """Function to handle the movement of agents around the canvas
    
    Method Arguments:
    * agent: The zombie/human agent that will be updated and moved
    * vec:
    * mag:
    
    Output:
    * An updated x, y location for the agent based on set conditions
    """
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
        human = Human(speed)
        human.plot = plt.Circle(newPos(), radius, color=color_human)
        list_humans.append(human)
        if visual:
            ax.add_artist(human.plot)
    for i in range(pop_zombie):
        speed = calculateSpeed(speed_zombie, zombie_spread)
        zombie = Zombie(speed)
        zombie.plot = plt.Circle(newPos(), radius, color=color_zombie)
        list_zombies.append(zombie)
        if visual:
            ax.add_artist(zombie.plot)
    for i in range(water_stores):
        c = plt.Circle(newPos(), radius, color=color_water)
        water.append(c)
        if visual:
            ax.add_artist(c)

def moveZombies():
    """Function to handle the movement of zombie agents around
    the canvas and to properly decay the zombie agents. Zombie agents attempt to 
    reach the closest human in their range of sight
    
    Output:
    * Calls the move() function for the zombie agent
    """
    global decayed
    decayed = []
    
    humanCenters = np.array([human.plot.center for human in list_humans])
    for zombie in list_zombies:
        zombie = zombie.decay() # decay
        if zombie.time_till_death == 0:
            decayed.append(zombie)
        dist = zombie_range_sq # zombie range of sight ** 2
        vec = (0., 0.)
        
        # distances between the humans and zombie agents
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
    """Helper function to handle the zombie agents that have reached
    their time limit and need to be removed
    
    Output:
    * an updated list of zombies, and the removal of the decayed zombie agents
    from the canvas
    """
    for zombie in decayed:
        list_zombies.remove(zombie)
        if visual:
            zombie.remove()

def moveAndInfectHumans():
    """Function to move the human agents away from the zombie agents. If a 
    zombie agent touches a human then that human becomes infected   
    
    Output:
    * Calls the move() function for the human agents.
    """
    global infected
    infected = []
    
    zombieCenters = np.array([zombie.plot.center for zombie in list_zombies])
    for human in list_humans:
        vec = (0., 0.)
        
        ydiff = wrapDiff(human.plot.center[0] - zombieCenters[:,0]) # Flipped?
        xdiff = wrapDiff(human.plot.center[1] - zombieCenters[:,1])
        sqdist = ydiff ** 2 + xdiff ** 2
        minDistIdx = np.argmin(sqdist)
        if sqdist[minDistIdx] < two_radius_sq: # zombie is touching a human
            infected.append(human) # add to infected, zombifyInfected() will handle
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
    """A method to handle the human agents that have been
    infected and will turn them into zombie agents
    
    Output:
    * An updated zombie list that now includes previously infected humans
    """
    for human in infected:
        list_humans.remove(human)
        speed = calculateSpeed(speed_zombie, zombie_spread)
        zombie = Zombie(speed)
        zombie.plot = human.plot
        zombie.plot.set_color(color_zombie)
        list_zombies.append(zombie)

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
            
            if len(list_zombies) != 0:
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
            if len(list_humans) == 0 or len(list_zombies) == 0:
                break
        
        #print 'humans: ' + str(len(list_humans)) + ' zombies: ' + str(len(list_zombies))
        if not go:
            break
    
