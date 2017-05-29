#==============================================================================
#                            General Documentation
#
"""
    This class represents the Water agents in the Zombie simulation. Each
    water agent starts out with available resources of 3.0. Water agents
    can be drained of resources via the drain() method which will return
    the amount that has been drained. max_level if that amount is available,
    or the current waterLevel if waterLevel < max_level. This amount will then
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

class Water:

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.radius = 10       
        self.waterLevel = 3.0

   
    def pos(self):
        return (self.y, self.x)

    #drains resources from a water agent. Each call of the function will
    #result in a drain of max_level in water resources if that amount is
    #available. Otherwise the rest of the water resource will be drained.
    #retVal returned is equal to the amount of water drained.
    def drain(self, max_level):
        retVal = 0.01
        if(self.waterLevel < max_level):
            self.waterLevel = self.waterLevel - max_level
        else:
            retVal = self.waterLevel
            self.waterLevel = 0.0
        return retVal