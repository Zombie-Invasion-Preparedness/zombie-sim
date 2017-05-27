#==============================================================================
#                            General Documentation
#
"""
    This class represents the Shelter agents in the Zombie simulation. Each
    shelter agent has a width and height, as well as a bottom, top, left, 
    and right side. Shelters can hold a certain number of humans, but can not 
    hold any zombies. If there is space for a human they may enter the
    building, and will be shown in the center of it, while zombies will 
    simply collide with the building and be unable to go inside. Shelters 
    can be in any shape or position, but for this simulation are in the 
    general shape of UWB's campus buildings. 
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

class Shelter:

    # ---------------------------- Global Agent Variables ----------------------

    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = x-width/2
        self.right = x+width/2
        self.bottom = y-height/2
        self.top = y+height/2
        
    # some methods require coordinates in a (y, x) form
    def pos(self):
        return (self.y, self.x)
    
    def colliding(self, x, y):
        """A function to determine if an agent is colliding with the shelter, this is called in the 
        move() function when an agent is moving
    
        Method Arguments:
        * x: The x position value of the agent that is moving
        * y: The y position value of the agent that is moving
    
        Output:
        * Returns whether or not the agent's x and y positions where colliding with 
        the shelter in question
        """
        return not (y < self.bottom or y > self.top or x < self.left or x > self.right)

    def collision(self, xFrom, yFrom, xTo, yTo, vec, mag):
        """A function to determine if an agent is colliding with a shelter
    
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
        ydiff = yTo - self.y
        xdiff = xTo - self.x
        if ydiff < xdiff:
            if ydiff < -xdiff:#collision on top
                #print("top")
                x = self.collisionOffset(xFrom, self.bottom - yFrom , vec[1], mag)
                y = self.bottom
            else: #collision on right
                #print("top " + str(xFrom)) 
                y = self.collisionOffset(yFrom ,xFrom - self.right, vec[0], mag)
                x = self.right
        else:
            if ydiff < -xdiff: #collision on 
                #print("left " + str(xFrom)) 
                y = self.collisionOffset(yFrom , self.left - xFrom, vec[0], mag)
                x = self.left
            else: #collision on 
                x = self.collisionOffset(xFrom, yFrom  - self.top, vec[1], mag)
                y = self.top
        return x,y

    def collisionOffset(self, start, lead, target, mag):
        """ A function to determine the offset values for an agent colliding with 
        a shelter object
        
        Method Arguments:
        * start: The starting position value, can be an x or y value
        * lead: The distance between the agent and the shelter
        * target: The x or y component of the vector from collision()
        * mag: The magnitude of vec
    
        Output:
        * Output vals
        """
        if mag == 0:
            print("UH OH!")
        
        ratio = lead / mag
        if target < 0:
            mag = -mag
        return (start + target * ratio + (1. - ratio) * mag)












