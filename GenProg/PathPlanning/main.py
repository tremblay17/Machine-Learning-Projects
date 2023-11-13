import sys, getopt
import fuzzyLogic
import pathPlanning
from matplotlib import pyplot as plt

def main(argv):
    opts, args = getopt.getopt(argv,"h:p:m:c:g:",["population=","mutationrate=",
                                                  "crossoverrate=","generations="])
    # if len(argv) != 4:
    #     "Usage: main.py populationSize mutationProb crossoverProb numOfGenerations"
    #     return 1
    for opt, arg in opts:
        pass
    
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])