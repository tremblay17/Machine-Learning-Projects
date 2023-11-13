import MLP
import numpy as np

mlp = MLP.MLP
inputs = np.array([[0,0],[0,1],[1,0],[1,1]]).reshape((4,2))
lr =0.1
epochs = 5
randVal = mlp.randomizeValues(mlp, numWeights=6,numNodes=3,numInputs=2)

weights = mlp.buildWeightMat(randVal)

weights = np.array(weights).reshape((3,2)) #[[w13,w23],[w14,w24],[w35,w45]]
thresholds = np.array(randVal[1]).reshape((3,1)) #[[t0],[t1],[t2]]

x=1
while(x <= epochs):
    hiddenOutput = mlp.sigmoid(mlp,inputs,weights,thresholds,True) #Calc hidden layer
    hiddenOutput = np.array(hiddenOutput).reshape(2,4)

    hiddenOutput = mlp.buildOutputMat(hiddenOutput)
    #print("Hidden Layer Activation: ",hiddenOutput)

    outputOutput = mlp.sigmoid(mlp,hiddenOutput,weights,thresholds,False) #Calc output layer
    outputOutput = outputOutput.reshape((4,1))
    #print("Output Layer Activation: ",outputOutput)

    errorMat = mlp.calcError(inputs,outputOutput) #Calc error for output layer
    #print("Error: ",errorMat.reshape((4,1)))

    outputEG = mlp.errorGradient(mlp, outputOutput,weights,False,errorMat)
    outputEG = outputEG.reshape(4,1)
    #print(outputEG)

    oldWeights = weights
    for weight in range(len(weights[-1])): #outputLayer
        weights[-1][weight] += mlp.deltaRule(lr, outputOutput[weight][0], outputEG[weight][0])
        thresholds[-1][0] += mlp.deltaRule(lr, outputOutput[weight][0], outputEG[weight][0])
    #print("Output Layer: ", weights[-1])

    hiddenEG = mlp.errorGradient(mlp, hiddenOutput,weights,True,[],outputEG)
    hiddenEG = hiddenEG.reshape(4,2)
    #print(hiddenEG)

    for weight in range(len(weights)-1): #hiddenLayer
        for j in range(len(weights[weight])):
            weights[weight][j] += mlp.deltaRule(lr, hiddenOutput[weight][j], hiddenEG[weight][j])
            thresholds[weight][0] += mlp.deltaRule(lr, hiddenOutput[weight][j], hiddenEG[weight][j])
    #print("Hidden Node1: ", weights[0])
    #print("Hidden Node2: ", weights[1])

    print("| Threshold: ", thresholds[-1][0], " | Learning Rate: ", lr, " |\n")
    print("| Epoch | Input 1 | Input 2 | Desired Out | Init Weight 1 | Init Weight 2 | Actual Out | Error e | Final Weight 1 | Final Weight 2 |\n")
    for i in range(len(inputs)):
        if((inputs[i][0] == 0 and inputs[i][1] == 1) or (inputs[i][0] == 1 and inputs[i][1] == 0)):
            d = 1
        else:
            d = 0
        print("| ", x, " | ", inputs[i][0], " | ", inputs[i][1], " | ",
              d, " | ",oldWeights[-1][0], " | ",oldWeights[-1][1], " | ",
              outputOutput[i][0], " | ",
              errorMat[i], " | ",
              weights[-1][0], " | ",weights[-1][1], " |\n")


    if(x == epochs):
        sumSquaredErr = 0
        for e in range(len(errorMat)):
            sumSquaredErr+=(errorMat[e])**2
        print("| Input 1 | Input 2 | Desired Out | Actual Out | Error e | Sum Squared Errors |\n")
        for i in range(len(inputs)):
            if((inputs[i][0] == 0 and inputs[i][1] == 1) or (inputs[i][0] == 1 and inputs[i][1] == 0)):
                d = 1
            else:
                d = 0
            print("| ",inputs[i][0], " | ",inputs[i][1]," | ",d, " | ",outputOutput[i][0], " | ",errorMat[i], "| ", sumSquaredErr, "|\n")
    x+=1
trainArray = np.array([])
trainArray = np.append(trainArray, weights)
trainArray = np.append(trainArray, thresholds)
#print(trainArray)

for i in range(len(inputs)):
    hiddenOutput = mlp.sigmoid(mlp, inputs,weights,thresholds,True)
    hiddenOutput = np.array(hiddenOutput).reshape(2,4)

    hiddenOutput = mlp.buildOutputMat(hiddenOutput)

    outputOutput = mlp.sigmoid(mlp, hiddenOutput, weights, thresholds, False)
print("Input: ", inputs[0], inputs[1], inputs[2], inputs[3])
print("Prediction: ", outputOutput)
