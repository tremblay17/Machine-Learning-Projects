import math
import numpy as np
import matplotlib.pyplot as plt

def binary_to_decimal(binary_str):
    return int(binary_str, 2)

def decode_chromosome(chromosome):
    num_bits = len(chromosome) // 2
    x_binary = chromosome[:num_bits]
    y_binary = chromosome[num_bits:]
    
    x = -3 + (6 / (2 ** num_bits - 1)) * binary_to_decimal(x_binary)
    y = -3 + (6 / (2 ** num_bits - 1)) * binary_to_decimal(y_binary)
    
    return x, y

def fitness_function(x, y):
    return ((1 - x)**2) * (math.e**(-(x**2) - (y + 1)**2)) - (x - x**3 - y**3) * (math.e**(-(x**2) - y**2))

def roulette_wheel_selection(population, fitness_values):
    total_fitness = np.sum(fitness_values)
    probabilities = fitness_values / total_fitness
    probabilities = np.maximum(probabilities, 0)
    probabilities /= np.sum(probabilities)
    selected_indices = np.random.choice(len(population), size=len(population), p=probabilities)
    selected_population = [population[i] for i in selected_indices]
    return selected_population

def crossover(parent1, parent2, crossover_rate):
    if np.random.rand() < crossover_rate:
        crossover_point = np.random.randint(1, len(parent1))
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    else:
        return parent1, parent2

def mutate(chromosome, mutation_rate):
    mutated_chromosome = list(chromosome)
    for i in range(len(mutated_chromosome)):
        if np.random.rand() < mutation_rate:
            mutated_chromosome[i] = '1' if chromosome[i] == '0' else '0'
    return ''.join(mutated_chromosome)

def genetic_algorithm(population_size, num_generations, crossover_rate, mutation_rate):
    num_bits = 8
    population = [''.join(np.random.choice(['0', '1'], size=num_bits * 2)) for _ in range(population_size)]
    
    avg_fitnesses = []
    best_fitnesses = []
    
    for generation in range(num_generations):
        decoded_population = [decode_chromosome(chromosome) for chromosome in population]
        fitness_values = [fitness_function(x, y) for x, y in decoded_population]
        
        avg_fitness = np.mean(fitness_values)
        best_fitness = np.max(fitness_values)
        
        avg_fitnesses.append(avg_fitness)
        best_fitnesses.append(best_fitness)
        
        # Select parents using roulette wheel selection
        selected_population = roulette_wheel_selection(population, fitness_values)
        
        # Create the next generation
        new_population = []
        for i in range(0, population_size, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i + 1]
            
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            
            new_population.extend([child1, child2])
        
        population = new_population
    
    # Find the best solution in the final population
    final_decoded_population = [decode_chromosome(chromosome) for chromosome in population]
    final_fitness_values = [fitness_function(x, y) for x, y in final_decoded_population]
    best_solution_index = np.argmax(final_fitness_values)
    best_solution = final_decoded_population[best_solution_index]
    best_fitness = final_fitness_values[best_solution_index]
    
    return best_solution, best_fitness, avg_fitnesses, best_fitnesses
'''
Set the parameters here for:
Population Size, Number of Generations to run,
Crossover and Mutation Rate
'''
popSize = 60
gens = 20
crossRate = 0.7
mutationRate = 0.0001

best_solution, best_fitness, avg_fitnesses, best_fitnesses = genetic_algorithm(
    population_size=popSize, num_generations=gens, crossover_rate=crossRate, mutation_rate=mutationRate
)
for fitness in range(len(avg_fitnesses)):
    avg_fitnesses[fitness]-=min(avg_fitnesses)
for fitness in range(len(best_fitnesses)):
    best_fitnesses[fitness]-=min(best_fitnesses)

print("Best solution:", best_solution)
print("Best fitness:", best_fitness)

# Plotting
generation_numbers = np.arange(1, len(avg_fitnesses) + 1)
plt.plot(generation_numbers, avg_fitnesses, label="Average Fitness")
plt.plot(generation_numbers, best_fitnesses, label="Best Fitness")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.legend()
plt.show()
