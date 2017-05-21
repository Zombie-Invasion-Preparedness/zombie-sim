import random

class Human:

    min_food = 0.3 # minimum starting food
    min_water = 0.3 # minimum starting water
    max_food = 1.0 # maximum starting food
    max_water = 1.0 # maximum starting wtaer
    thirsty = .7 # look for water
    hungry = .7 # look for food
    max_consumption = 0.01 # max can eat/drink at one tick

    def __init__(self, speedLvl):
        self.speed = speedLvl
        self.set_levels()

    def set_levels(self):
        self.calc_food()
        self.calc_water()
        self.calc_resource_usage()
        return self
    
    # determine how much food to start with
    def calc_food(self):
        global min_food
        global max_food
        self.food = random.uniform(Human.min_food, Human.max_food)
        return self

    # determine how much water to start with
    def calc_water(self):
        self.water = random.uniform(Human.min_water, Human.max_water)
        return self

    # find out the human's resource usage
    def calc_resource_usage(self):
        self.dehydrate_rate = self.speed / 2 # proportional to speed
        self.starve_rate = self.speed / 2
        return self

    # food used
    def starve(self):
        self.food = self.food - self.starve_rate
        return self

    # water used
    def dehydrate(self):
        self.water = self.water - self.dehydrate_rate
        return self

    # use energy
    def expire(self):
        self.starve()
        self.dehydrate()
        return self

    # eat
    def eat(self, amount):
        if(amount > Human.max_consumption):
            self.food = self.food + Human.max_consumption
        else:
            self.food = self.food + amount
        return self

    # drink
    def drink(self, amount):
        if(amount > Human.max_consumption):
            self.water = self.water + Human.max_consumption
        else:
            self.water = self.water + amount
        return self
