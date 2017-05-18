import random

class Zombie:

    min_hours_till_death = 100.0
    max_hours_till_death = 200.0

    def __init__(self, speedLvl):
        self.speed = speedLvl
        self.set_levels()

    def set_levels(self):
        self.set_decay_rate()
        self.set_time_till_death()

    def set_decay_rate(self):
        self.decay_rate = random.uniform(0.5, 1.5)
        return self

    def set_time_till_death(self):
        self.time_till_death = random.randint(Zombie.min_hours_till_death, Zombie.max_hours_till_death)
        return self

    def decay(self):
        self.time_till_death = self.time_till_death - self.decay_rate
        return self