# ==============================================================================
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

# ------------------------------------------------------------------------------
#                           Additional Documentation
#
#   Authors:    Destiny Boyer, Taran Christensen, Scott Ferguson, Jeremy Luxon
#   Date:       5/21/2017
#   Class:      CSS 458 - Computer Simulation
#   Assignment: Final Project, Zombie Simulation
# ==============================================================================

import numpy


class Food:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.height = 10
        self.foodLevel = 5.0
        self.depleted = False

        self.calculate_coordinates()

    def coordinates(self):
        return [self.left, self.top, self.right, self.bottom]

    def calculate_coordinates(self):
        self.left = [self.x - self.height, self.y]
        self.top = [self.x, self.y + self.height]
        self.right = [self.x + self.height, self.y]
        self.bottom = [self.x, self.y - self.height]
        return self

    def pos(self):
        return (self.y, self.x)

    def colliding(self, x, y, radius):
        """A function to determine if an agent is colliding with the food agent,
        this is called in the move() function when an agent is moving

        Method Arguments:
        * x: The x position value of the agent that is moving
        * y: The y position value of the agent that is moving

        Output:
        * Returns whether or not the agent's x and y positions where colliding with 
        the food agent in question
        """
        return not (y + radius < self.bottom[1] or y - radius > self.top[1] or
                    x + radius < self.left[0] or x - radius > self.right[0])

    # drains resources from a food agent. Each call of the function will
    # result in a drain of max_level in food resources if that amount is
    # available. Otherwise the rest of the food resource will be drained.
    # retVal returned is equal to the amount of food drained.

    def drain(self, amtEaten):
        self.foodLevel = self.foodLevel - amtEaten
        self.color = [self.color[0], min(int(self.color[1] * 1.2), 255), min(int(self.color[2] * 1.5), 255)]
        if (self.foodLevel <= 0):
            self.depleted = True
            self.color = [0, 0, 0]
        return self

    # some methods require coordinates in a (y, x) form
    def pos(self):
        return (self.y, self.x)
