import numpy as np
import matplotlib.pyplot as plt

# Constants
NUM_UNITS = 7
NUM_INTERVALS = 4
MAX_LOADS = [80, 90, 65, 70]

# Unit data: [unit_capacity, maintenance_intervals]
UNITS_DATA = {
    1: [20, 2],
    2: [15, 2],
    3: [35, 1],
    4: [40, 1],
    5: [15, 1],
    6: [15, 1],
    7: [10, 1]
}

# Genetic Algorithm Parameters
POPULATION_SIZE = 50
NUM_GENERATIONS = 100
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.01

# Helper functions
def binary_to_decimal(binary_str):
    return int(binary_str, 2)

def decode_chromosome(chromosome):
    decoded_schedule = []
    for i in range(0, len(chromosome), 4):
        unit_schedule = binary_to_decimal(chromosome[i:i+4])
        decoded_schedule.append(unit_schedule)
    return decoded_schedule

def encode_chromosome(schedule):
    encoded_chromosome = ""
    for unit_schedule in schedule:
        encoded_chromosome += format(unit_schedule, '04b')
    return encoded_chromosome

# Genetic Algorithm
def generate_initial_population():
    return [''.join(np.random.choice(['0', '1'], size=4).astype(str)) for _ in range(POPULATION_SIZE)]

def fitness_function(chromosome):
    decoded_schedule = [decode_chromosome(chromosome[i:i+4]) for i in range(0, len(chromosome), 4)]

    net_reserve = np.zeros(NUM_INTERVALS)
    for unit, intervals in enumerate(decoded_schedule):
        for interval in intervals:
            interval = max(0, min(interval, NUM_INTERVALS - 1))  # Ensure interval is within valid range
            net_reserve[interval] += UNITS_DATA[unit + 1][0]

    penalty = np.maximum(MAX_LOADS - net_reserve, 0)
    return -np.max(penalty)

def roulette_wheel_selection(population, fitness_values):
    total_fitness = np.sum(fitness_values)
    probabilities = fitness_values / total_fitness
    selected_indices = np.random.choice(len(population), size=len(population), p=probabilities)
    selected_population = [population[i] for i in selected_indices]
    return selected_population

def crossover(parent1, parent2):
    if np.random.rand() < CROSSOVER_RATE:
        crossover_point = np.random.randint(1, len(parent1))
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    else:
        return parent1, parent2

def mutate(chromosome):
    mutated_chromosome = list(chromosome)
    for i in range(len(mutated_chromosome)):
        if np.random.rand() < MUTATION_RATE:
            mutated_chromosome[i] = '1' if chromosome[i] == '0' else '0'
    return ''.join(mutated_chromosome)

def genetic_algorithm():
    population = generate_initial_population()
    avg_fitnesses = []
    best_fitnesses = []

    for generation in range(NUM_GENERATIONS):
        fitness_values = np.array([fitness_function(chromosome) for chromosome in population])

        avg_fitness = np.mean(fitness_values)
        best_fitness = np.max(fitness_values)

        avg_fitnesses.append(avg_fitness)
        best_fitnesses.append(best_fitness)

        selected_population = roulette_wheel_selection(population, fitness_values)

        new_population = []
        for i in range(0, POPULATION_SIZE, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i + 1]

            child1, child2 = crossover(parent1, parent2)

            child1 = mutate(child1)
            child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = np.array(new_population)

    best_solution_index = np.argmax(fitness_values)
    best_solution = population[best_solution_index]

    return best_solution, best_fitnesses, avg_fitnesses

# Run the genetic algorithm
best_solution, best_fitnesses, avg_fitnesses = genetic_algorithm()

# Print the best solution and its fitness
decoded_best_solution = [decode_chromosome(best_solution[i:i+4]) for i in range(0, len(best_solution), 4)]
print("Best Solution:")
for unit, interval in enumerate(decoded_best_solution):
    print(f"Unit {unit + 1}: Interval {interval}")

print("Best Fitness:", fitness_function(best_solution))
for i in range(len(avg_fitnesses)):
    avg_fitnesses[i] -= min(avg_fitnesses)
for i in range(len(best_fitnesses)):
    best_fitnesses[i] -= min(best_fitnesses)
# Plotting
generation_numbers = np.arange(1, NUM_GENERATIONS + 1)
plt.plot(generation_numbers, avg_fitnesses, label="Average Fitness")
plt.plot(generation_numbers, best_fitnesses, label="Best Fitness")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend()
plt.show()
