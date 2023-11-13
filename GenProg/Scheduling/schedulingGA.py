#Constraints:
#Max Loads: 1|80 2|90 3|65 4|70
#TotalLoad - LoadInMaintenance >= MaxLoad
#FitnessFunc = TotLoad - LoadInMaintenance
#Chromosomes 4 bits:
#Unit  Possibilities
#1     1100 0110 0011    
#2     1100 0110 0011 
#3     1000 0100 0010 0001
#4     1000 0100 0010 0001
#5     1000 0100 0010 0001
#6     1000 0100 0010 0001
#7     1000 0100 0010 0001

from ctypes import sizeof
from random import randint


class ScheduleGA:
    def __init__(self):
        self.unit1 = [[1,1,0,0],[0,1,1,0],[0,0,1,1]]
        self.unit2 = [[1,1,0,0],[0,1,1,0],[0,0,1,1]]
        self.unit3 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.unit4 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.unit5 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.unit6 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        self.unit7 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        pass
    def fitFunc(self, chromsome, totLoad, maxLoad, workLoad, popSize):
        pass
    def mutate(self, child):
        pass
    def crossover(self, parent1, parent2):
        #Take child 1 = first 4 gene-sets p1 + last 3 gene-sets p2
        #Take child 2 = first 4 gene-sets p2 + last 3 gene-sets p1
        pass
    def randNum(self, unit):
        if unit >2:
            return randint(0,3)
        return randint(0,2)
    def binToDec(self, chromosome):
        #Translate each gene into a value
        pass
    def evaluate(self,population=[]): 
        for i in range(10):
            for j in range(len(population)):
                tmp = population[j]
                population.remove(j)
                pass
            return tmp
        return population
        
    def population(self, first, popSize, geneLength, numUnits, population = None):
        population = []
        i = 0
        while(i != popSize):
            parent = []
            topParents = []
            realValues = []
            if first:
                parent.append(self.unit1[self.randNum(1)])
                parent.append(self.unit2[self.randNum(2)])
                parent.append(self.unit3[self.randNum(3)])
                parent.append(self.unit4[self.randNum(4)])
                parent.append(self.unit5[self.randNum(5)])
                parent.append(self.unit6[self.randNum(6)])
                parent.append(self.unit7[self.randNum(7)])
                if(self.checkConstraints(parent)):
                    population.append(parent)
            #top = self.findTopFitness(population)
            #self.crossover(parent1,parent2)
            i+=1
    def checkConstraints(self, parent):
        pass