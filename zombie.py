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
#   Authors:    Destiny Boyer, Taran Christensen, Scott Ferguson, Jeremy Luxon
#   Date:       5/18/2017
#   Class:      CSS 458 - Computer Simulation
#   Assignment: Final Project, Zombie Simulation
#==============================================================================

#-------------------- Module General Import and Declarations ------------------
import random

class Zombie:

    # ---------------------------- Global Agent Variables ----------------------

    # starting time limit for zombies
    min_hours_till_death = 100.0
    max_hours_till_death = 200.0

    def __init__(self, speedLvl, color, x, y):
        self.color = color
        self.x = x
        self.y = y

        self.speed = speedLvl
        self.set_levels()

    # some methods require coordinates in a (y, x) form
    def pos(self):
        return (self.y, self.x)

    def set_levels(self):
        self.set_decay_rate()
        self.set_time_till_death()
        self.set_strength()
        return self
        
    def eat(self, energy):
        self.time_till_death = self.time_till_death + energy
        return self

    # set the decay rate
    def set_decay_rate(self):
        self.decay_rate = random.uniform(0.5, 1.5)
        return self

    def set_strength(self):
        self.strength = random.randint(0, 5)
        return self

    # set the time left for a zombie
    def set_time_till_death(self):
        self.time_till_death = random.randint(Zombie.min_hours_till_death, Zombie.max_hours_till_death)
        return self

    # increment a zombies time left by its rate of decay
    def decay(self):
        self.time_till_death = self.time_till_death - self.decay_rate
        return self

    def encounter(self, power):
        if(self.strength > power):
            return True
        else:
            return False