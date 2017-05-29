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

import numpy

class Food:

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.height = 10
        self.foodLevel = 1.0

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
        """A function to determine if an agent is colliding with the shelter, this is called in the 
        move() function when an agent is moving
    
        Method Arguments:
        * x: The x position value of the agent that is moving
        * y: The y position value of the agent that is moving
    
        Output:
        * Returns whether or not the agent's x and y positions where colliding with 
        the shelter in question
        """
        return not (y + radius < self.bottom[1] or y - radius > self.top[1] or
            x + radius < self.left[0] or x - radius > self.right[0])

    def collision(self, xFrom, yFrom, xTo, yTo, vec, mag, radius):
        """ Determines the resulting position of an agent colliding with
        this shelter
    
        Method Arguments:
        * xFrom: The current x value of the agent
        * yFrom: The current y value of the agent
        * xTo: The x value the agent would like to travel to
        * yTo: The y value the agent would like to travel to
        * vec: The vector that is made from the agents position and the shelter position
        * mag: The magnitude of vec
    
        Output:
        * Return the new x and y values for the colliding agent
        """
        if xTo >= self.x:
            xdiff = xTo - self.right[0]
        else:
            xdiff = xTo - self.left[0]
        if yTo >= self.y:
            ydiff = yTo - self.top[1]
        else:
            ydiff = yTo - self.bottom[1]
        if xTo >= self.x and ((yTo >= self.y and xdiff >= ydiff) or (yTo < self.y and xdiff >= -ydiff)):
            #collision on right
            y = self.collisionOffset(yFrom, xFrom - self.right[1], vec[0], mag)
            x = self.right[0] + radius
        elif yTo >= self.y and ((xTo >= self.x and ydiff >= xdiff) or (xTo < self.x and xdiff >= -ydiff)):
            #collision on top
            x = self.collisionOffset(xFrom, yFrom  - self.top[0], vec[1], mag)
            y = self.top[1] + radius
        elif xTo < self.x and ((yTo >= self.y and xdiff < -ydiff) or (yTo < self.y and xdiff < ydiff)):
            #collision on left
            y = self.collisionOffset(yFrom, self.left[1] - xFrom, vec[0], mag)
            x = self.left[0] - radius
        else:
            #collision on bottom
            x = self.collisionOffset(xFrom, self.bottom[0] - yFrom, vec[1], mag)
            y = self.bottom[1] - radius
        return x, y


    def collisionOffset(self, start, lead, target, mag):
        """ Determines the resulting value of a coordinate of an agent along a
        colliding edge of this shelter
        
        Method Arguments:
        * start: The starting position value, can be an x or y value
        * lead: The distance before the agent will collide with the shelter
        * target: The target destination x or y coordinate
        * mag: The total magnitude of the movement vector
    
        Output:
        * Resulting position coordinate along colliding edge of shelter
        """
        ratio = lead / mag
        if target < 0:
            mag = -mag
        return (start + target * ratio + (1. - ratio) * mag)

    #drains resources from a food agent. Each call of the function will
    #result in a drain of max_level in food resources if that amount is
    #available. Otherwise the rest of the food resource will be drained.
    #retVal returned is equal to the amount of food drained.
    def drain(self, amtEaten):
        self.foodLevel = self.foodLevel - amtEaten
        self.color = [min(int(self.color[0]*1.1), 255), min(int(self.color[1]*1.1), 255), min(int(self.color[2]*1.1), 255)]
        return self
        
    # some methods require coordinates in a (y, x) form
    def pos(self):
        return (self.y, self.x)