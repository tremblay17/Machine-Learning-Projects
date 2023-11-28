'''
Write a program in Python or the language of your choice that does the following scheduling using Genetic Algorithms.
You would need to upload your code and the output that it generates in form of a Fitness/Generations graph for best and average values, as you can see below and in the slides.

Scheduling of 7 power units in 4 equal intervals.

    The problem Constraints:
        The maximum loads expected during four intervals are 80, 90, 65 and 70 MW;
        Maintenance of any unit starts at the beginning of an interval and finishes at the end of the same or adjacent interval. The maintenance cannot be aborted or finished            earlier than scheduled;
        The net reserve of the power system must be greater or equal to zero at any interval.

    The optimum criterion is the maximum of the net  reserve at any maintenance period.

    Unit data and maintenance requirement:
    
            Unit 1: Capacity 20 MW, maintenance interval 2
            Unit 2: Capacity 15 MW, maintenance interval 2
            Unit 3: Capacity 35 MW, maintenance interval 1
            Unit 4: Capacity 40 MW, maintenance interval 1
            Unit 5: Capacity 15 MW, maintenance interval 1
            Unit 6: Capacity 15 MW, maintenance interval 1
            Unit 7: Capacity 10 MW, maintenance interval 1
    
    Possible schedules for each unit: 

            Unit 1: 1100 | 0110 | 0011
            Unit 2: 1100 | 0110 | 0011
            Unit 3: 1000 | 0100 | 0010 | 0001 
            Unit 4: 1000 | 0100 | 0010 | 0001 
            Unit 5: 1000 | 0100 | 0010 | 0001 
            Unit 6: 1000 | 0100 | 0010 | 0001 
            Unit 7: 1000 | 0100 | 0010 | 0001 
'''
import random
import matplotlib.pyplot as plt
import numpy as np

# Define the power units and their capacities and maintenance intervals
units = [
    {"capacity": 20, "maintenance": ['1100', '0110', '0011']},
    {"capacity": 15, "maintenance": ['1100', '0110', '0011']},
    {"capacity": 35, "maintenance": ['1000', '0100', '0010', '0001']},
    {"capacity": 40, "maintenance": ['1000', '0100', '0010', '0001']},
    {"capacity": 15, "maintenance": ['1000', '0100', '0010', '0001']},
    {"capacity": 15, "maintenance": ['1000', '0100', '0010', '0001']},
    {"capacity": 10, "maintenance": ['1000', '0100', '0010', '0001']}
]

# Define the maximum loads for each interval
max_loads = [80, 90, 65, 70]

# Define the population size and number of generations
pop_size = 100
generations = 50

# Define the crossover and mutation probabilities
crossover_probability = 0.7
mutation_probability = 0.01

# Initialize the population with random schedules
population = [[random.choice(unit["maintenance"]) for unit in units] for _ in range(pop_size)]

# Define the fitness function
def fitness(schedule):
    # Initialize an empty list to store the reserves for each interval
    reserves = []

    # Iterate over each interval
    for j, load in enumerate(max_loads):
        # Calculate the total capacity for the current interval
        total_capacity = sum(max(int(schedule[i][j]) * units[i]["capacity"], 0) for i in range(len(units)))

        # Calculate the reserve for the current interval and add it to the reserves list
        reserve = total_capacity - load
        reserves.append(reserve)

    # The fitness is the maximum reserve
    return max(reserves)

# Run the GA for a set number of generations
best_fitness = []
avg_fitness = []
for _ in range(generations):
    # Evaluate the fitness of each schedule in the population
    fitnesses = [fitness(schedule) for schedule in population]

    # Record the best and average fitness
    best_fitness.append(max(fitnesses))
    avg_fitness.append(sum(fitnesses) / len(fitnesses))

    # Select the best schedules for reproduction
    parents = [population[i] for i in sorted(range(len(fitnesses)), key=lambda i: fitnesses[i])[-pop_size//2:]]

    # Use crossover to produce child schedules
    children = []
    for _ in range(pop_size):
        if random.random() < crossover_probability:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            crossover_point = random.randint(0, len(units))
            child = parent1[:crossover_point] + parent2[crossover_point:]
            # Check if the new schedule results in all units being in maintenance
            # or if the total capacity of units not in maintenance is less than the maximum load
            if sum(int(child[i][j]) for i in range(len(units)) for j in range(4)) != 4:
                # Check if the total capacity of units not in maintenance is greater than the maximum load for each interval
                for interval in range(4):
                    if sum(units[i]["capacity"] for i, unit_schedule in enumerate(child) if unit_schedule[interval] == '0') < max_loads[interval]:
                        break
                else:
                    # If the total capacity of units not in maintenance is greater than the maximum load for all intervals, add the child to the new population
                    children.append(child)
        else:
            child = random.choice(parents)
            children.append(child)

    # Use mutation to randomly alter the child schedules
    for child in children:
        if random.random() < mutation_probability:
            mutate_point = random.randint(0, len(units) - 1)
            new_schedule = random.choice(units[mutate_point]["maintenance"])
            # Check if the new schedule results in all units being in maintenance
            # or if the total capacity of units not in maintenance is less than the maximum load
            if sum(int(new_schedule[i]) for i in range(4)) != 4 or sum(int(child[i][j]) for i in range(len(units)) for j in range(4)) - sum(int(child[mutate_point][j]) for j in range(4)) > 0:
                # Check if the total capacity of units not in maintenance is greater than the maximum load for each interval
                for interval in range(4):
                    if sum(units[i]["capacity"] for i, unit_schedule in enumerate(child) if unit_schedule[interval] == '0') < max_loads[interval]:
                        break
                else:
                    # If the total capacity of units not in maintenance is greater than the maximum load for all intervals, apply the mutation
                    child[mutate_point] = new_schedule

    # Replace the population with the new children
    population = children
for i in population:
    print(i)
# Plot the best and average fitness over generations
plt.plot(best_fitness, label="Best Fitness")
plt.plot(avg_fitness, label="Average Fitness")
plt.legend()
plt.show()