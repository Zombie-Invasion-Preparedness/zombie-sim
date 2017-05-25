#==============================================================================
#                            General Documentation
#
"""
    This class represents the Human agents in the Zombie simulation. Human
    agents are created by declaring an agent and passing in a speed level.
    The newly created agent uses this speed level in conjunction with the
    globally defined data members to set appropriate resource usage rates.
    Food and water levels are calculated randomly for each Human object
    based on global data members.
"""

#------------------------------------------------------------------------------
#                           Additional Documentation
#
#   Authors:    Destiny Boyer, Taran Christensen, Scott Ferguson, Jeremy Luxon
#   Date:       5/18/2017
#   Class:      CSS 458 - Computer Simulation
#   Assignment: Final Project, Zombie Simulation
#==============================================================================

#-------------------- Module General Import and Declarations ------------------

import random

class Human:

    # ---------------------------- Global Agent Variables ----------------------
    
    min_food = 0.3          #- minimum starting food
    min_water = 0.3         #- minimum starting water
    max_food = 1.0          #- maximum starting food
    max_water = 1.0         #- maximum starting water
    thirsty = .7            #- look for water
    hungry = .7             #- look for food
    max_consumption = 0.01  #- max can eat/drink at one tick
    in_shelter = False      #- whether this human is inside
    destination = (0,0)     #- location destination when safe

    def __init__(self, speedLvl, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.distractions = 0
        self.speed = speedLvl
        self.set_levels()

    # some methods require coordinates in a (y, x) form
    def pos(self):
        return (self.y, self.x)

    def set_levels(self):
        self.calc_food()
        self.calc_water()
        self.calc_resource_usage()
        return self
    
    # determine how much food to start with
    def calc_food(self):
        self.food = random.uniform(Human.min_food, Human.max_food)
        return self

    # determine how much water to start with
    def calc_water(self):
        self.water = random.uniform(Human.min_water, Human.max_water)
        return self

    # find out the human's resource usage
    def calc_resource_usage(self):
        self.dehydrate_rate = self.speed / 2 # proportional to speed
        self.starve_rate = self.speed / 2
        return self

    # food used
    def starve(self):
        self.food = self.food - self.starve_rate
        return self

    # water used
    def dehydrate(self):
        self.water = self.water - self.dehydrate_rate
        return self

    # use energy
    def expire(self):
        self.starve()
        self.dehydrate()
        return self

    # eat
    def eat(self, amount):
        if(amount > Human.max_consumption):
            self.food = self.food + Human.max_consumption
        else:
            self.food = self.food + amount
        return self

    # drink
    def drink(self, amount):
        if(amount > Human.max_consumption):
            self.water = self.water + Human.max_consumption
        else:
            self.water = self.water + amount
        return self

    # not yet polished function for moving human agents. Seeks food if food is
    # below hungry and food is below water. Otherwise if water is below food and
    # the agent is hungry, the agent will seek water. Else the agent seeks food.
    # However, we need to account for zombies being near as well.
    def move(self):
        if(self.food < hungry and self.food < self.water):
            seek_food()
        elif(self.water < thirsty and self.water < self.food):
            seek_water()
        else:
            seek_shelter()

    def distract_zombie(self):
        if(self.distractions > 0):
            self.distractions = self.distractions - 1
            return random.randint(0,10)
        else:
            return 0

