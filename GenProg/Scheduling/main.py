import random
import sys, getopt
import matplotlib
from matplotlib import pyplot as plt
import genericGA
#import schedulingGA
def main(argv)->int: #Population, mutation rate, crossover rate, generations
    population =100
    generations =250
    mutationProb =0.001
    crossoverProb =0.7
    opts, args = getopt.getopt(argv,"h:p:m:c:g:",["population=","mutationrate=",
                                                  "crossoverrate=","generations="])
    # if len(argv) != 4:
    #     "Usage: main.py populationSize mutationProb crossoverProb numOfGenerations"
    #     return 1
    for opt, arg in opts:
        if opt == "-h":
            print("-p | --population=\n"
                  "-m | --mutationrate=\n"
                  "-c | --crossoverrate=\n"
                  "-g | --generations=\n")
            sys.exit()
        elif opt in ("-p", "population"):
            population=int(arg)
        elif opt in ("-m", "mutationrate"):
            mutationProb=float(arg)
        elif opt in ("-c","crossoverrate"):
            crossoverProb=float(arg)
        elif opt in ("-g","--generations"):
            generations=int(arg)
    print('population size: ',population,'\nprobability of mutation: ',mutationProb,'\nprobability of crossover: ', crossoverProb,'\nnumber of generations: ',generations,'\n')
    genAlgo = genericGA.genericGA(population,generations,mutationProb,crossoverProb)
    axisData = genAlgo.runPopulation()
    
    
    line1 = axisData[0] #Avg Fitness levels
    line2 = axisData[1] #Best Fitness levels
    x = [i for i in range(generations)]
    plt.axes()
    plt.plot(x, line1,line2)
    plt.show()
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])