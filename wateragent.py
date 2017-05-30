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
        self.waterLevel = 8.0
        self.depleted = False

   
    def pos(self):
        return (self.y, self.x)

    def colliding(self, x, y, aRadius):
        """A function to determine if an agent is colliding with a water agent,
        this is called in the move() function when an agent is moving
    
        Method Arguments:
        * x: The x position value of the agent that is moving
        * y: The y position value of the agent that is moving
        * radius: The radius of the moving agent
    
        Output:
        * Returns whether or not the agent's x and y positions where colliding with 
        the water agent in question
        """
        xdiff = x - self.x
        ydiff = y - self.y

        sqdist = xdiff ** 2 + ydiff ** 2
        diff = sqdist ** (1./2)
        
        return diff <= (aRadius + self.radius)

    #drains resources from a water agent. Each call of the function will
    #result in a drain of max_level in water resources if that amount is
    #available. Otherwise the rest of the water resource will be drained.
    #retVal returned is equal to the amount of water drained.
    def drain(self, amtEaten):
        self.waterLevel = self.waterLevel - amtEaten
        self.color = [self.color[0], min(int(self.color[1]*1.5), 255), min(int(self.color[2]*1.9), 255)]
        if(self.waterLevel <= 0):
            self.color = [0,0,0]
            self.depleted = True
        return self
