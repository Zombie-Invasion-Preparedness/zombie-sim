#===============================================================================
#                            General Documentation
#
"""
    This class represents the driver for the zombie simulation. Its purpose is 
    to instantiate the shelter, food, water, human, and zombie agents. It will 
    also start the instance of pygame that will visualize the simulation.
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
from shelter import Shelter
from foodagent import Food
from wateragent import Water
import pygame

#---------------------------- User defined variables ---------------------------
visual = True
runs = 1                # times to run the sim
pop_human = 100         # initial population of humans
pop_zombie = 20         # initial population of zombies
water_stores = 6        # number of water locations
food_stores = 6         # number of food locations
shelter_locs = 5        # number of shelter locations
UWBConfiguration = True # UW Bothell building configuration
speed_human = 1.75      # base speed of humans
speed_zombie = 2.0      # base speed of zombies
human_spread = .35      # spread of human speed
zombie_spread = .25     # variance in speed of humans/zombies
zombie_range = 175      # zombie range of sight
radius = 5

#------------------------------ Constant variables -----------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WATER_COLOR = (0, 191, 255)
FOOD_COLOR = [255, 128, 0]
YELLOW = (255, 255, 0)

# used in the main loop
two_radius_sq = (radius * 2) ** 2
zombie_range_sq = zombie_range ** 2

# screen dimensions
WIDTH = 1024
HEIGHT = 768


# edges of the square, with radius offset
left = 0. - radius
right = WIDTH + radius
top = 0.0 + radius
bottom = HEIGHT - radius

#------------------------------- Global variables ------------------------------
list_humans = []        # holds the human objects
list_zombies = []       # holds the zombie objects
list_water = []         # holds water objects
list_food = []          # holds food objects
list_shelters = []      # holds shelter objects
list_water = []

water = []
infected = []
decayed = []

#-------------------------------- Helper Methods -------------------------------

def newPos():
    """ Generate a new valid random starting position for an agent

    Output:
    * A two element array consisting of two random floats that correspond to a
    position that does not lie within any shelter 
    """
    while True:
        pos = np.random.random(2) * (HEIGHT, WIDTH)
        valid = True
        for shelter in list_shelters:
            if shelter.colliding(pos[1], pos[0], radius):
                valid = False
                break
        if valid:
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

def move(agent, vec, mag):
    """Function to handle the movement of agents around the canvas

    Method Arguments:
    * agent: The zombie/human agent that will be updated and moved
    * vec: The vector that is made from the agents position and its destination
    * mag: The magnitude of vec

    Output:
    * An updated x, y location for the agent based on set conditions
    """
    
    y = (agent.y + vec[0]) % HEIGHT
    x = (agent.x + vec[1]) % WIDTH

    # If we're in a shelter, don't call collision
    if agent.__class__.__name__ == "Human":
        if agent.in_shelter:
            agent.y = y
            agent.x = x
            return

    for shelter in list_shelters:
        if shelter.colliding(x, y, radius):
            x, y = shelter.collision(agent.x, agent.y, x, y, vec, mag, radius)
            if agent.__class__.__name__ == "Human":
                agent.in_shelter = True
            break # Here we make the assumption that we will only collide once

    for food in list_food:
        if food.colliding(x, y, radius):
            x, y = food.collision(agent.x, agent.y, x, y, vec, mag, radius)
            if agent.__class__.__name__ == "Human":
                agent.near_food = True
                agent.foodAgent = food
            break

    for water in list_water:
        if water.colliding(x, y, radius):
            if agent.__class__.__name__ == "Human":
                agent.near_water = True
                agent.waterAgent = water
            break

    agent.y = y
    agent.x = x

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
    
def initializeLevel():
    """A function that initializes all level pieces, such as shelters to be is the rough shape of the 
    UWB campus (per Lin's suggestion)

    Output:
    * Outputs the level scene to have building objects in the rough shape of the UWB campus
    """

    # if we should draw the UWB campus
    if UWBConfiguration:
        xPos = 0
        yPos = 100
        list_shelters.append(Shelter(GRAY, 280 + xPos, 150 + yPos, 175, 50)) # UW2
        list_shelters.append(Shelter(GRAY, 400 + xPos, 75 + yPos, 50, 200))  # DISC
        list_shelters.append(Shelter(GRAY, 280 + xPos, 310 + yPos, 200, 50)) # UW1
        list_shelters.append(Shelter(GRAY, 458 + xPos, 310 + yPos, 50, 50))  # LBA
        list_shelters.append(Shelter(GRAY, 512 + xPos, 240 + yPos, 150, 50)) # LB1
        list_shelters.append(Shelter(GRAY, 612 + xPos, 335 + yPos, 50, 100)) # LB2
        list_shelters.append(Shelter(GRAY, 512 + xPos, 416 + yPos, 50, 75))  # ARC
        list_shelters.append(Shelter(GRAY, 800 + xPos, 310 + yPos, 200, 50)) # CC1
        list_shelters.append(Shelter(GRAY, 900 + xPos, 150 + yPos, 75, 75))  # CC3-1
        list_shelters.append(Shelter(GRAY, 820 + xPos, 133 + yPos, 75, 40))  # CC3-2
    else:
        for i in range(shelter_locs):
            y, x = newPos()
            size = np.random.random(2)*20 + 100
            shelter = Shelter(GRAY, x, y, size[0], size[1])
            list_shelters.append(shelter)
        
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

def initializeResources():
    """ A function that initializes a given number of water and food
        resource agents.

    Output:
    *   Each class will have a number of food and water agents, these
        will be initialized and added to the simulation.
    """
    for i in range(food_stores):
            y, x = newPos()
            food = Food(FOOD_COLOR, x, y)
            list_food.append(food)

    for i in range(water_stores):
            y, x = newPos()
            water = Water(WATER_COLOR, x, y)
            list_water.append(water)

def zombifyInfected():
    """A method to handle the human agents that have been
    infected and will turn them into zombie agents

    Output:
    * An updated zombie list that now includes previously infected humans
    """
    for human in infected:
        list_humans.remove(human)
        human.speed = np.random.normal(speed_zombie, zombie_spread) # new speed
        zombie = Zombie(human.speed, RED, human.x, human.y)         # make a new zombie agent at the human's location
        zombie.set_time_till_death()                                # set the new time of death
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
    humanCenters[np.array([human.infected_tic for human in list_humans]) > 0] = [-100,-100]
    for zombie in list_zombies:
        zombie.decay()  # decay
        if zombie.time_till_death < 0: # cant use == 0
            decayed.append(zombie)
        dist = zombie_range_sq  # zombie range of sight ** 2
        vec = (0., 0.)

        # distances between the humans and zombie agents
        ydiff = wrapDiffY(humanCenters[:, 0] - zombie.y)
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
    global infected, decayed
    infected = []
    
    zombieCenters = np.array([zombie.pos() for zombie in list_zombies])
    shelterCenters = np.array([shelter.pos() for shelter in list_shelters])
    for human in list_humans:
        vec = (0., 0.)

        human.expire() # use food/water
        if human.infected_tic == 0:
            infected.append(human)

        # Shelter differences
        ydiffSh = wrapDiffY(shelterCenters[:, 0] - human.y)
        xdiffSh = wrapDiffX(shelterCenters[:, 1] - human.x)
        sqdistSh = ydiffSh ** 2 + xdiffSh ** 2
        closestShIdx = np.argmin(sqdistSh)

        # Skip running from zombies if this human is inside
        if not human.in_shelter:
            # Zombie differences        
            ydiffZ = wrapDiffY(human.y - zombieCenters[:, 0])  # Flipped?
            xdiffZ = wrapDiffX(human.x - zombieCenters[:, 1])
            sqdistZ = ydiffZ ** 2 + xdiffZ ** 2
            minDistIdx = np.argmin(sqdistZ)

            # Check nearest zombie's distance for infection chance
            if sqdistZ[minDistIdx] < two_radius_sq:
                power = human.distract_zombie()
                if list_zombies[minDistIdx].encounter(power):
                    human.color = YELLOW
                    human.infect()
                    #infected.append(human)
                else:
                    list_zombies.remove(list_zombies[minDistIdx]) # skip decay step
                    zombieCenters = np.array([zombie.pos() for zombie in list_zombies])
                    #decayed.append(list_zombies[minDistIdx])

            if sqdistZ[minDistIdx] > sqdistSh[closestShIdx]: # A shelter is closer than a zombie
                
                if(human.food < Human.hungry and human.food < human.water):     # if human needs food
                    vec = moveToFood(human)
            
                elif(human.water < Human.thirsty and human.water < human.food):     # if human needs water
                    vec = moveToWater(human)

                else:
                    # Move towards the shelter
                    vec = (ydiffSh[closestShIdx] / sqdistSh[closestShIdx],
                        xdiffSh[closestShIdx] / sqdistSh[closestShIdx])
            else:
                # Move away from all zombies
                vec = (np.sum(ydiffZ / sqdistZ), np.sum(xdiffZ / sqdistZ))
                
            mag = np.sqrt(vec[0] ** 2 + vec[1] ** 2) / human.speed
        
        elif human.destination != (0, 0): # if in a shelter and has a spot
            if np.allclose((human.y, human.x), human.destination, atol=1):
                continue # Skip moving this human if it's comfy

            if(human.food < Human.hungry and human.food < human.water):     # if human needs food    
                vec = moveToFood(human)
            
            elif(human.water < Human.thirsty and human.water < human.food):     # if human needs water
                vec = moveToWater(human)

            else:
                vec = (wrapDiffY(human.destination[0] - human.y),
                       wrapDiffX(human.destination[1] - human.x))
            mag = np.sqrt(vec[0] ** 2 + vec[1] ** 2) / (human.speed/2)
        else: # find a spot in the shelter
            xOffset = np.random.uniform(list_shelters[closestShIdx].left + 10,
                                        list_shelters[closestShIdx].right - 10)
            yOffset = np.random.uniform(list_shelters[closestShIdx].bottom + 10,
                                        list_shelters[closestShIdx].top - 10)
            human.destination = (yOffset, xOffset)
            vec = (wrapDiffY(yOffset - human.y),wrapDiffX(xOffset - human.x))
            
            mag = np.sqrt(vec[0] ** 2 + vec[1] ** 2) / (human.speed/2)
        move(human, (vec[0] / mag, vec[1] / mag), human.speed)

def eatAndDrink():
    for human in list_humans:  
        if human.near_food is True:
            amtEaten = human.eat(human.foodAgent.foodLevel)
            human.foodAgent.drain(amtEaten)
            human.near_food = False
            human.foodAgent = None

        if human.near_water is True:
            amtDrank = human.drink(human.waterAgent.waterLevel)
            human.waterAgent.drain(amtDrank)
            human.near_water = False
            human.foodAgent = None

def moveToWater(human):
    waterCoor = np.array([water.pos() for water in list_water])
    ydiffWater = wrapDiffY(waterCoor[:, 0] - human.y)
    xdiffWater = wrapDiffX(waterCoor[:, 1] - human.x)
    sqdistWater = ydiffWater ** 2 + xdiffWater ** 2
    closestWaterIdx = np.argmin(sqdistWater)

    return (ydiffWater[closestWaterIdx] / sqdistWater[closestWaterIdx],  # move towards closest water agent
        xdiffWater[closestWaterIdx] / sqdistWater[closestWaterIdx])

def moveToFood(human):
    foodCoor = np.array([food.pos() for food in list_food])
    ydiffFood = wrapDiffY(foodCoor[:, 0] - human.y)
    xdiffFood = wrapDiffX(foodCoor[:, 1] - human.x)
    sqdistFood = ydiffFood ** 2 + xdiffFood ** 2
    closestFoodIdx = np.argmin(sqdistFood)

    return (ydiffFood[closestFoodIdx] / sqdistFood[closestFoodIdx],  # move towards closest food agent
                        xdiffFood[closestFoodIdx] / sqdistFood[closestFoodIdx])


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
        pygame.display.set_caption('Team ZIP Zombie-Invasion Simulation') # set the caption of the pygame window


        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

    # main simulation loop
    for i in range(runs):

        # create the human and zombie circles
        initializePopulations()
        initializeResources()
        initializeLevel()

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
                eatAndDrink()
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
                for sprite in list_shelters:
                    pygame.draw.rect(screen, sprite.color, pygame.Rect(int(sprite.left), int(sprite.bottom), int(sprite.width), int(sprite.height)))      

                for sprite in list_humans + list_zombies:
                    pygame.draw.circle(screen, sprite.color, (int(sprite.x), int(sprite.y)), radius)

                for sprite in list_food:
                    pygame.draw.polygon(screen, sprite.color, sprite.coordinates())


                for sprite in list_water:
                    pygame.draw.circle(screen, sprite.color,(int(sprite.x), int(sprite.y)), sprite.radius) 
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


