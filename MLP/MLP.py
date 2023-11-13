import random as rand
import numpy as np


class MLP:
    def ___init___(self) -> None:
        pass
    def sigmoid(self, inputs, weights, thresholds, hidden):
        activationMat = np.array([])
        #y_j(p) = nΣi=1(x_i(p)w_ij(p)-Θ_j) Hidden Layer
        #for hiddenNeuron in range(len(weights)-1)
            #for inputFromInput in range(inputs)
                #y += (input*weight-threshold)
        if(hidden is not False):
            for i in range(len(weights)-1): #Calculates output for all inputs per hidden node
                y=0
                #print("weight:", i, weights[i])
                #print("curr out: ", y)
                for j in range(len(inputs)): #For all inputs
                    for k in range(len(inputs[j])): #For a single input
                        y += ((inputs[j][k]*weights[i][k]-thresholds[i][0]))
                        #print("input: ", j, " ",k, " output: ", y)
                    #print("sum: ", y)
                    activationMat = np.append(activationMat, y)
            return activationMat #returns array with shape (2,4)
        #y_k(p) = mΣj=1(x_jk(p)w_jk(p)-Θ_k) Output layer
        #for outputNeuron in range(len(weights)-2)
            #for inputFromHidden in range(inputs)
                # y += (input*weight-threshold)
                
        for i in range(len(weights)-2): #Calculates output for all inputs per output node
            y=0
            #print("calc output layer: ")
            #print("weight:", i, weights[i])
            #print("curr out: ", y)
            for j in range(len(inputs)): #For all inputs
                y=0
                for k in range(len(inputs[j])): #For a single input
                    y += ((inputs[j][k]*weights[-1][k]-thresholds[-1][0]))
                    #print("input: ", j, " ",k)
                #print("output: ", y)
                activationMat = np.append(activationMat, y)
        return activationMat #returns array with shape (4,)
    def calcError(inputArr, actual):
        #e(p) = Y_desired(p)-Y_actual(p)
        errorMat = np.array([])
        
        for i in range(len(actual)):
            if((inputArr[i][0]==0 and inputArr[i][1]==1) or (inputArr[i][0]==1 and inputArr[i][1]==0)):
                desired = 1
            else:
                desired = 0
            actualVal = actual[i][0]
            errorMat = np.append(errorMat,(desired-actualVal))
        return errorMat
    
    def errorGradient(self,sigmoidOutput, weights, hidden, errorMat=[], previousGradientMat=[]):
        #δ_k(p) = y_k(p)*[1-y_k(p)]*e_k(p) Output | sigmoid*(1-sigmoid)*error
        gradientMat = np.array([])
        if(hidden is False):
            for i in range(len(errorMat)):
                eg = (sigmoidOutput[i][0]*
                      (1-sigmoidOutput[i][0])*
                      errorMat[i])
                gradientMat = np.append(gradientMat, eg)
            return gradientMat
        #δ_j(p) = y_j(p)*[1-y_j(p)]*lΣk=1(δ_k(p)*w_jk(p)) Hidden | 
        for i in range(len(previousGradientMat)):
            gradientSum = 0
            for j in range(len(weights[-1])):
                gradientSum += previousGradientMat[i][0]*weights[-1][j]
        #for i in range(len(previousGradientMat)):
            gradient = [sigmoidOutput[i][0]*(1-sigmoidOutput[i][0])*gradientSum, sigmoidOutput[i][1]*(1-sigmoidOutput[i][1])*gradientSum]
            gradientMat = np.append(gradientMat, gradient)
        return gradientMat
    def sumSquaredErrors(): #Sum of Squared Errors
        pass
    def deltaRule(lr, input_sigmoidOutput, gradientOutput): #learning rule
        #Δw_jk(p) = (α)*(y_j(p))*(δ_k(p))) Output | lr*(sigmoid)*(errorGradient)
        #w_jk(p+1) = w_jk(p) + Δw_jk(p) Output | 
        delta = lr*input_sigmoidOutput*gradientOutput
        return delta
        #Δw_ij(p) = (α)*(x_i(p))*(δ_j(p))) Hidden | lr*(inputs)*(errorGradient)
        #w_ij(p+1) = w_ij(p) + Δw_ij(p) Hidden | 
    def printEpochs():
        pass
    def randomizeValues(self, numWeights=6, numNodes=3, numInputs=2):
        #initialize weights and Θ [+/-(2.4/totInputs)] 
        #returns mat = [[w13 w23 ...], [Θ3 Θ4 ...]]
        randVals = []
        weightMat = []
        thresholdMat = []
        for x in range(numWeights):
            weightMat.append(rand.uniform((-2.4/numInputs),(2.4/numInputs)))
        for y in range(numNodes):
            thresholdMat.append(rand.uniform((-2.4/numInputs),(2.4/numInputs)))
        randVals.append(weightMat)
        randVals.append(thresholdMat)   
        return randVals
    def buildWeightMat(valMat):
        weights =[]
        tmp = []
        for x in range(0,len(valMat[0]),2):
            tmp.append(valMat[0][x])
            tmp.append(valMat[0][x+1])
            weights.append([tmp[0],tmp[1]])
            tmp.clear()
        return weights
    def buildOutputMat(valMat):
        tmp = valMat
        valMat = np.array([])
        valMat = np.append(valMat, [tmp[0][0],tmp[1][0]])
        valMat = np.append(valMat, [tmp[0][1],tmp[1][1]])
        valMat = np.append(valMat, [tmp[0][2],tmp[1][2]])
        valMat = np.append(valMat, [tmp[0][3],tmp[1][3]])
        valMat = valMat.reshape(4,2)
        return valMat
        
