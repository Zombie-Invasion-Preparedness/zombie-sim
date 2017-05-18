import random

class Human:

	min_food = 0.3
	min_water = 0.3
	max_food = 1.0
	max_water = 1.0
	max_consumption = 0.01

	def __init__(self, speedLvl):
		self.speed = speedLvl
		self.set_levels()

	def set_levels(self):
		self.food = calculate_level(min_food, max_food)
		self.water = calculate_level(min_water, max_water)
		self.calc_food()
		self.calc_water()
		self.calc_resource_usage()

	def calc_food(self):
		self.food = random.uniform(min_food, max_food)
		return self

	def calc_water(self):
		self.water = random.uniform(min_water, max_water)
		return self

	def calc_resource_usage(self):
		self.dehydrate_rate = self.speed / 2
		self.starve_rate = self.speed / 2
		return self

	def starve(self):
		self.food = self.food - self.starve_rate
		return self

	def dehydrate(self):
		self.water = self.water - self.dehydrate_rate
		return self

	def expire(self):
		self.starve()
		self.dehydrate()
		return sel

	def eat(self, amount):
		if(amount > max_consumption):
			self.food = self.food + max_consumption
		else:
			self.food = self.food + amount
		return self

	def drink(self, amount):
		if(amount > max_consumption):
			self.water = self.water + max_consumption
		else:
			self.water = self.water + amount
		return self
