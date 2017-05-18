#==============================================================================
#                            General Documentation
#
"""
    This class represents the Zombie agents in the Zombie simulation. Zombie
    agents are created by declaring an agent and passing in a speed level.
    Each agent calculates a random number of hours until death based on a 
    range specified in the Global Agent Variables section.
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

class Zombie:

    #---------------------------- Global Agent Variables ----------------------

    min_hours_till_death = 100.0
    max_hours_till_death = 200.0

    def __init__(self, speedLvl):
        self.speed = speedLvl
        self.set_levels()

    def set_levels(self):
        self.set_decay_rate()
        self.set_time_till_death()

    def set_decay_rate(self):
        self.decay_rate = random.uniform(0.5, 1.5)
        return self

    def set_time_till_death(self):
        self.time_till_death = random.randint(Zombie.min_hours_till_death, Zombie.max_hours_till_death)
        return self

    def decay(self):
        self.time_till_death = self.time_till_death - self.decay_rate
        return self