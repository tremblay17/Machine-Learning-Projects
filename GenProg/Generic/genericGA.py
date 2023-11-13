import math
import numpy as np
import random as rand
import pandas as pd

#rand.seed(42)
class genericGA:
    global globProbabilityMatrix

    def __init__(self, populationSize, generations, mutationRate, crossoverRate):
        self.populationSize = populationSize
        self.generations = generations
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.geneLength = 16
    def numConversion(self, numToConv, isBin=False, toArray=False):
        if(isBin and not toArray): #if numToConv is binary convert to base 10
            return int(numToConv,2)
        if(isBin and toArray): #Converts string into array of ints
            strToInt = []
            for char in numToConv:
                int(char)
                strToInt.append(char)
            #strToInt.append(intArr)
            return strToInt
        if(not isBin and toArray): #Converts array of ints into string
            intToStr = ''
            for num in numToConv:
                intToStr+=str(num)
            return intToStr
        return np.base_repr(numToConv) #converts base 10 to binary otherwise
    def arrConversion(self, binStr): #Converts binary string into an array of 2 elements [[x][y]]
        arr = []
        str1 =''
        str2 =''
        i=0
        while(i<len(binStr)):
            if i < len(binStr)/2:#First 8 bits of binary string =x
                str1 += binStr[i]
            if i >= len(binStr)/2:#Last 8 bits of binary string =y
                str2 += binStr[i]
            i+=1
        arr.append(str1)
        arr.append(str2)
        return arr #Array [x,y] is returned
    
    def generateChromosome(self, numGenes): #Generates a chromosome as a binary string
        binStr = ''
        for i in range(numGenes):
            binStr+=str(rand.getrandbits(1))
        return binStr   
    def generatePopulation(self, popSize): #Generates a population
        population = []
        for i in range(popSize):
            population.append(self.generateChromosome(self.geneLength))
        return population
    
    def normalize(self,gene, popSize): #Encodes the gene to a value between -3 & 3
        formula = 6/((2**len(gene))-1)
        gene = self.numConversion(gene, True) #Converts gene to base 10
        #print("Function: normalize\n"
        #      "Variable: gene", gene, '\n')
        return round(gene*formula-3,5)
    def fitFunc(self, chromosome): #Calculates the fitness of a chromosome
        c = self.arrConversion(chromosome)
        #print("Function: fitFunc\n",
        #      "Variable: c", c, '\n')
        x = c[0]
        y = c[1]
        x = self.normalize(x,self.populationSize)
        y = self.normalize(y,self.populationSize)
        #((1-x)^2)*(e^(-(x^2)-((y+1)^2)))-(x-(x^3)-(y^3))*(e^(-(x^2)-(y^2)))
        return ((1-x)**2)*(math.e**(-(x**2)-((y+1)**2)))-(x-(x**3)-(y**3))*(math.e**(-(x**2)-(y**2)))
    
    def evaluate(self, population): #Evaluates performance of a population
        totalFitness = 0
        fitnessArr = []
        for chromosome in population:
            x = self.fitFunc(chromosome)
            fitnessArr.append(x)
            totalFitness+=x
            ##print(totalFitness)
        averageFitness = totalFitness/len(population)
        return totalFitness,fitnessArr,averageFitness
    def selection(self, population, totalFitness, fitnessArray): #Roulette wheel selection, determines chromosomes to mate
        #Calculate Ratios
        rouletteWheel = [round(i/totalFitness,5) for i in fitnessArray]

        #Calculate Cumulative Probabilities
        cumProb = [rouletteWheel[0]]
        for prob in rouletteWheel[1:]:
            cumProb.append(prob+cumProb[-1])
        #Pick a random value 
        randNum = rand.choice(cumProb)
        choose = 0
        chromosomeIndex =0
        for prob in cumProb:
            choose += prob
            if choose >=randNum:
                global globProbabilityMatrix 
                globProbabilityMatrix = cumProb
                return population[chromosomeIndex] 
            else:
                chromosomeIndex += 1
    def selectionV2(self, population, totalFitness, fitnessArray): #Roulette wheel selection, determines chromosomes to mate
        global globProbabilityMatrix
        rouletteWheel = [i/totalFitness for i in fitnessArray]

        cumProb = [rouletteWheel[0]]
        for prob in rouletteWheel[1:]:
            cumProb.append(prob+cumProb[-1])

        globProbabilityMatrix = cumProb
        selectedChromosomes = rand.choices(population,(cumProb), k =2)
        
        return selectedChromosomes
    def crossover(self, population, totalFitness, fitnessArray): #mating function
        #chromosome = self.selection(population,totalFitness,fitnessArray) #Parent1
        #chromosome2 = self.selection(population,totalFitness,fitnessArray) #Parent2
        parents = self.selectionV2(population,totalFitness,fitnessArray)
        chromosome = parents[0]
        chromosome2 = parents[1]

        crossPointX = rand.randint(1,(len(chromosome)//2))
        crossPointY = rand.randint((len(chromosome)//2)+1,len(chromosome))
        #print("Cross Points | X: ",crossPointX,'\n',
        #      "Cross Points | Y: ",crossPointY, '\n')
        convArr = self.numConversion(chromosome,True,True) 
        #print("Function: crossover\n"
        #      "Variable: convArr", convArr, '\n')
        convArr2 = self.numConversion(chromosome2, True,True)
        #print("Function: crossover\n"
        #      "Variable: convArr2", convArr2, '\n')
        #print('\n',convArr,' ',chromosome,)
        #print('\n',convArr2,' ',chromosome2)
        newC1 = (convArr[:crossPointX-1] + convArr2[crossPointX-1:(len(chromosome)//2)] + 
                 convArr[(len(chromosome)//2):crossPointY-1] + convArr2[crossPointY-1:])

        newC2 = (convArr2[:crossPointX-1] + convArr[crossPointX-1:(len(chromosome)//2)] + 
                 convArr2[(len(chromosome)//2):crossPointY-1] + convArr[crossPointY-1:])

        #print("C1: ", newC1, "\nC2: ", newC2)
        newC1 = self.numConversion(newC1,False,True)
        #print("Function: crossover\n"
        #      "Variable: newC1", newC1, '\n')
        newC2 = self.numConversion(newC2,False,True)
        #print("Function: crossover\n"
        #      "Variable: newC2", newC2, '\n')
        return newC1,newC2
        #''.join(str(index) for index in array) this code will convert the array of int to a single string

    def mutation(self, population, mutationRate): #Randomly selects a gene of a chromosome in x & y
        #print(globProbabilityMatrix)
        selected =[]
        for chromosome in range(len(population)):
            if rand.uniform(0,1) <= mutationRate:
                #selected = chromosome
                selected = self.numConversion(population[chromosome],True,True)
                for i in range(len(selected)//2):
                    if (rand.uniform(0,1) <= mutationRate):
                        selected[i] == 1 if selected[i] == 0 else 0
                for j in range(len(selected)//2, len(selected)):
                    if (rand.uniform(0,1) <= mutationRate):
                        selected[j] == 1 if selected[j] == 0 else 0
                selected = self.numConversion(selected,False,True)
                population[chromosome] = selected
                break
        return population
        #''.join(str(index) for index in array) #Convert the array of int to a two strings for each parameter [['x']['y']]

    def runPopulation(self):
        #Generate initial population of random chromosomes
        #Evaluate
        #Selection
        #Crossover
        #New Population
        #Mutation
        #New Population w/ Mutations
        #Repeat
        avgFitArr = []
        bestFitArr = []
        bestFitness = -999
        lowestFitness = 999
        for i in range(self.generations):
            if i == 0: 
                population = self.generatePopulation(self.populationSize)
            #for c in population:
            #    print(c)
            #print('\n')
            newPopulation = []
            evaluation = self.evaluate(population)
            totalFitness = evaluation[0]
            fitnessArray = evaluation[1]
            averageFitness = evaluation[2]
            if(max(fitnessArray)>bestFitness):
                bestFitness = max(fitnessArray)
                bestPopulation = population
            if(min(fitnessArray)<lowestFitness):
                lowestFitness = min(fitnessArray)
            for j in range(len(population)//2):
                newChildren = self.crossover(population,totalFitness,fitnessArray)
                newPopulation.append(newChildren[0])
                newPopulation.append(newChildren[1])
            
            newChildren = []
            #for c in newPopulation:
            #    print(c)
            #print('\n')
            for j in range(len(population)):
                newPopulation = self.mutation(population, self.mutationRate)
            #newPopulation = self.mutation(population, self.mutationRate)
            population = newPopulation
            #for c in population:
            #    print(c)
            #print('\n')
            avgFitArr.append(averageFitness)
            bestFitArr.append(bestFitness)
        #For all fitness, subtract lowest fitness (negative) to make all >=0        
        for i in avgFitArr:
            i -= lowestFitness
        for i in bestFitArr:
            i -= lowestFitness
        # print("Best Population: ")
        # for i in bestPopulation:
        #     print(i)
        print("Population Size: ", len(population))
        print("\nTotal Fitness: ", totalFitness)
        print("\nAvg Fitness: ", averageFitness)
        print("\nBest Fitness: ", bestFitness)
        print("\nLowest Fitness: ", lowestFitness)
        return avgFitArr,bestFitArr
    
        