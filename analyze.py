import numpy as np
import matplotlib.pyplot as plt

class Analyze:
   
    def __init__(self,model):
        self.model = model
        
    def plotAvgNums(self):
        
        # Determine max length of a population array
        length = len(sorted(self.model.zombie_time_pop,key=len, reverse=True)[0])
        
        # Determine our timestep x axis
        timeSteps = np.arange(length)
        
        # Pad array to be a square matrix, filled with 0's for missing values 
        avgZoms = np.array([xi+[0]*(length-len(xi)) for xi in self.model.zombie_time_pop])
        avgHums = np.array([xi+[0]*(length-len(xi)) for xi in self.model.human_time_pop])
        avgInf = np.array([xi+[0]*(length-len(xi)) for xi in self.model.infected_time_pop])
        
        # Average out values
        avgZoms = np.mean(avgZoms,0)
        avgHums = np.mean(avgHums,0)
        avgInf = np.mean(avgInf,0)
    
    
        plt.plot(timeSteps,avgZoms)
        plt.hold()
        plt.plot(timeSteps,avgHums)
        plt.plot(timeSteps,avgInf)
        