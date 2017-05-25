#==============================================================================
#                            General Documentation
#
"""
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
        """Docstring
    
        Method Arguments:
        * x: 
        * y:
    
        Output:
        * Output vals
        """
        return not (y < self.bottom or y > self.top or x < self.left or x > self.right)

    def collision(self, xFrom, yFrom, xTo, yTo, vec, mag):
        """Docstring
    
        Method Arguments:
        * xFrom: 
        * yFrom:
        * xTo:
        * yTo:
        * vec:
        * mag:
    
        Output:
        * Output vals
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
        """Docstring
    
        Method Arguments:
        * start: 
        * lead:
        * target:
        * mag:
    
        Output:
        * Output vals
        """
        if mag == 0:
            print("UH OH!")
        
        ratio = lead / mag
        if target < 0:
            mag = -mag
        return (start + target * ratio + (1. - ratio) * mag)












