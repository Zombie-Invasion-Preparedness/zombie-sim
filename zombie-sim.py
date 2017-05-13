"""
zombie-sim.py
"""

import numpy as np
import matplotlib.pyplot as plt

"""
parameters
"""
pop_human = 40
pop_zombie = 12
speed_human = .004
speed_zombie = .0044
zombie_life = 200
zombie_range = .35
radius = .01

"""
constants
"""
color_human = (0., 1., 0.)
color_zombie = (1., 0., 0.)

# used in the main loop
two_radius_sq = (radius * 2) ** 2
zombie_range_sq = zombie_range ** 2

# edges of the square, with radius offset
left = .4 - radius
right = .6 + radius
top = .6 + radius
bottom = .4 - radius

# global to stop the main loop if needed
go = True

"""
helper methods
"""

# listener for key press events
def on_key_press(event):
    global go
    if event.key == ' ': # if space is pressed, stop the sim
        go = False

# generate a new random circle starting position
def newPos():
    while True:
        pos = np.random.random(2)
        if pos[0] < bottom or pos[0] > top or pos[1] < left or pos[1] > right:
            return pos

def wrapDiff(diff):
    if diff > .5:
        return -1. + diff
    if diff < -.5:
        return 1. + diff
    return diff

def collisionOffset(start, lead, target, mag):
    ratio = lead / mag
    if target < 0:
        mag = -mag
    return (start + target * ratio + (1. - ratio) * mag) % 1.

def move(circle, vec, mag):
    y = (circle.center[0] + vec[0]) % 1.
    x = (circle.center[1] + vec[1]) % 1.
    if not (y < bottom or y > top or x < left or x > right):
        ydiff = y - .5
        xdiff = x - .5
        if ydiff < xdiff:
            if ydiff < -xdiff:
                x = collisionOffset(circle.center[1], bottom - circle.center[0], vec[1], mag)
                y = bottom
            else:
                y = collisionOffset(circle.center[0], circle.center[1] - right, vec[0], mag)
                x = right
        else:
            if ydiff < -xdiff:
                y = collisionOffset(circle.center[0], left - circle.center[1], vec[0], mag)
                x = left
            else:
                x = collisionOffset(circle.center[1], circle.center[0] - top, vec[1], mag)
                y = top
    circle.center = (y, x)

"""
main program code
"""

# create the figure
fig = plt.figure(figsize=(10, 8))
fig.canvas.mpl_connect('key_press_event', on_key_press)

# create the main axes
ax = fig.add_axes((0., 0., .8, 1.))
# todo: add some stats on the side

# create square wall in the middle
# todo: use more complex walls
rect = plt.Rectangle((.4, .4), .2, .2, color=(.5, .5, .5))
ax.add_artist(rect)

# create the human and zombie circles
humans = []
zombies = []
for i in range(pop_human):
    c = plt.Circle(newPos(), radius, color=color_human)
    humans.append(c)
    ax.add_artist(c)
for i in range(pop_zombie):
    c = plt.Circle(newPos(), radius, color=color_zombie)
    c.life = zombie_life
    zombies.append(c)
    ax.add_artist(c)

plt.show()

# main simulation loop
while go:
    decayed = []
    for zombie in zombies:
        zombie.life -= 1
        if zombie.life == 0:
            decayed.append(zombie)
        dist = zombie_range_sq
        vec = (0., 0.)
        for human in humans:
            ydiff = wrapDiff(human.center[0] - zombie.center[0])
            xdiff = wrapDiff(human.center[1] - zombie.center[1])
            sqdist = ydiff ** 2 + xdiff ** 2
            if sqdist < dist:
                dist = sqdist
                vec = (ydiff, xdiff)
        dist = np.sqrt(dist) / speed_zombie
        move(zombie, (vec[0] / dist, vec[1] / dist), speed_zombie)
    for zombie in decayed:
        zombies.remove(zombie)
        zombie.remove()
    if len(zombies) != 0:
        infected = []
        for human in humans:
            vec = (0., 0.)
            for zombie in zombies:
                ydiff = wrapDiff(human.center[0] - zombie.center[0])
                xdiff = wrapDiff(human.center[1] - zombie.center[1])
                sqdist = ydiff ** 2 + xdiff ** 2
                vec = (vec[0] + ydiff / sqdist, vec[1] + xdiff / sqdist)
                if sqdist < two_radius_sq:
                    infected.append(human)
                    break
            mag = np.sqrt(vec[0] ** 2 + vec[1] ** 2) / speed_human
            move(human, (vec[0] / mag, vec[1] / mag), speed_human)
        for human in infected:
            humans.remove(human)
            human.set_color(color_zombie)
            human.life = zombie_life
            zombies.append(human)
    plt.pause(.01)
    plt.draw()
    if len(zombies) == 0:
        break
