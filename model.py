#==============================================================================
#                            General Documentation
#
"""
    This class contains all of the models and model configurations that we
    used in the simulation. Each model has global configuration variables
    to specify the conditions that we are testing. When each model is
    instantiated it has object specific data structures to collect all the 
    data for each iteration that it is run for. This data can then be
    analyzed on a per model basis.
"""

#------------------------------------------------------------------------------
#                           Additional Documentation
#
#   Authors:    Destiny Boyer, Taran Christensen, Scott Ferguson, Jeremy Luxon
#   Date:       5/29/2017
#   Class:      CSS 458 - Computer Simulation
#   Assignment: Final Project, Zombie Simulation
#==============================================================================

import numpy

class DefaultModel:
	#----------------------- User-Defined Model Variables ---------------------

	UWB_CONFIG = True		#- building configuration
	NUM_RUNS = 100			#- number of simulation runs to log for this model
	NUM_WATER_AGENTS = 6	#- number of water agent locations
	NUM_FOOD_AGENTS = 6		#- number of food agent locations
	RESOURCE_CONFIG = 1		#- default random resource configuration
	HUMAN_SPEED = 1.75		#- human speed
	ZOMBIE_SPEED = 2.0		#- zombie speed
	HUMAN_SPREAD = 0.35		#- spread of human speed
	ZOMBIE_SPREAD = 0.25	#- spread of zombie speed
	ZOMBIE_RANGE = 175		#- 'sight' range of zombies
	ZOMBIE_POP = 20			#- beginning population of zombies
	HUMAN_POP = 100			#- beginning population of humans
	NUM_SHELTERS = 5		#- number of shelters available for humans

	#--------------------------------------------------------------------------


	def __init__(self):
		self.final_iter = numpy.zeros(NUM_RUNS)
		self.num_zomb = numpy.zeros(NUM_RUNS)
		self.count = 0;

	def log_data(nIter, nZombies):
		"""
		This method would log the data for each iteration run with the default
		model. This data would be added to the model object's data collection
		containers initialized in the __init__ method. So each Model would
		collect all the data for simulations of its type allowing for easy
		collection and analysis
		"""

		self.final_iter[self.count] = nIter
		self.num_zomb[self.count] = nZombies
		self.count = self.count + 1

class FastZombieModel:
	#----------------------- User-Defined Model Variables ---------------------

	UWB_CONFIG = True		#- building configuration
	NUM_RUNS = 100			#- number of simulation runs to log for this model
	NUM_WATER_AGENTS = 6	#- number of water agent locations
	NUM_FOOD_AGENTS = 6		#- number of food agent locations
	RESOURCE_CONFIG = 1		#- default random resource configuration
	HUMAN_SPEED = 1.75		#- human speed
	ZOMBIE_SPEED = 3.0		#- zombie speed
	HUMAN_SPREAD = 0.35		#- spread of human speed
	ZOMBIE_SPREAD = 0.25	#- spread of zombie speed
	ZOMBIE_RANGE = 175		#- 'sight' range of zombies
	ZOMBIE_POP = 20			#- beginning population of zombies
	HUMAN_POP = 100			#- beginning population of humans
	NUM_SHELTERS = 5		#- number of shelters available for humans

	#--------------------------------------------------------------------------


	def __init__(self):
		self.final_iter = numpy.zeros(NUM_RUNS)
		self.num_zomb = numpy.zeros(NUM_RUNS)
		self.count = 0;

	def log_data(nIter, nZombies):
		"""
		This method would log the data for each iteration run with the default
		model. This data would be added to the model object's data collection
		containers initialized in the __init__ method. So each Model would
		collect all the data for simulations of its type allowing for easy
		collection and analysis
		"""

		self.final_iter[self.count] = nIter
		self.num_zomb[self.count] = nZombies
		self.count = self.count + 1

class ResourceTwoModel:
	#-	This model has resources arranged in the resource configuation two
	#-	pattern

	#----------------------- User-Defined Model Variables ---------------------

	UWB_CONFIG = True		#- building configuration
	NUM_RUNS = 100			#- number of simulation runs to log for this model
	NUM_WATER_AGENTS = 6	#- number of water agent locations
	NUM_FOOD_AGENTS = 6		#- number of food agent locations
	RESOURCE_CONFIG = 1		#- default random resource configuration
	HUMAN_SPEED = 1.75		#- human speed
	ZOMBIE_SPEED = 3.0		#- zombie speed
	HUMAN_SPREAD = 0.35		#- spread of human speed
	ZOMBIE_SPREAD = 0.25	#- spread of zombie speed
	ZOMBIE_RANGE = 175		#- 'sight' range of zombies
	ZOMBIE_POP = 20			#- beginning population of zombies
	HUMAN_POP = 100			#- beginning population of humans
	NUM_SHELTERS = 5		#- number of shelters available for humans

	#--------------------------------------------------------------------------


	def __init__(self):
		self.final_iter = numpy.zeros(NUM_RUNS)
		self.num_zomb = numpy.zeros(NUM_RUNS)
		self.count = 0;

	def log_data(nIter, nZombies):
		"""
		This method would log the data for each iteration run with the default
		model. This data would be added to the model object's data collection
		containers initialized in the __init__ method. So each Model would
		collect all the data for simulations of its type allowing for easy
		collection and analysis
		"""

		self.final_iter[self.count] = nIter
		self.num_zomb[self.count] = nZombies
		self.count = self.count + 1