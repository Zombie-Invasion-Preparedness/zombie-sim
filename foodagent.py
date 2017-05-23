#==============================================================================
#                            General Documentation
#
"""
    This class represents the Food agents in the Zombie simulation. Each
    food agent starts out with available resources of 3.0. Food agents
    can be drained of resources via the drain() method which will return
    the amount that has been drained. max_level if that amount is available,
    or the current foodLevel if foodLevel < max_level. This amount will then
    be consumed by the human agent.
"""

#------------------------------------------------------------------------------
#                           Additional Documentation
#
#   Authors:    Destiny Boyer, Taran Christensen, Scott Ferguson, Jeremy Luxon
#   Date:       5/21/2017
#   Class:      CSS 458 - Computer Simulation
#   Assignment: Final Project, Zombie Simulation
#==============================================================================

class Food:

    def __init__(self):
        self.foodLevel = 3.0

    #drains resources from a food agent. Each call of the function will
    #result in a drain of max_level in food resources if that amount is
    #available. Otherwise the rest of the food resource will be drained.
    #retVal returned is equal to the amount of food drained.
    def drain(self, max_level):
        retVal = max_level
        if(self.foodLevel < max_level):
            self.foodLevel = self.foodLevel - max_level
        else:
            retVal = self.foodLevel
            self.foodLevel = 0.0
        return retVal