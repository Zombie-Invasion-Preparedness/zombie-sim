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
#   Authors:    Destiny Boyer, Taran Christensen, Scott Feurguson, Jeremy Luxom
#   Date:       5/18/2017
#   Class:      CSS 458 - Computer Simulation
#   Assignment: Final Project, Zombie Simulation
#==============================================================================

#-------------------- Module General Import and Declarations ------------------

import random

class Human:

    #---------------------------- Global Agent Variables ----------------------

    min_food = 0.3
    min_water = 0.3
    max_food = 1.0
    max_water = 1.0
    thirsty = .7 # look for water
    hungry = .7 # look for food
    max_consumption = 0.01

    def __init__(self, speedLvl):
        self.speed = speedLvl
        self.set_levels()

    def set_levels(self):
        self.calc_food()
        self.calc_water()
        self.calc_resource_usage()
        return self

	# determine how much food to start with
    def calc_food(self):
        global min_food
        global max_food
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
