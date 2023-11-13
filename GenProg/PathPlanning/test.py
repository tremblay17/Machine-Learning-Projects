import numpy as np
import pygame
import pygad
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Crop plot parameters
total_area = 1000  # Example total area (you can adjust this)
coverage_rate = 0.1  # Example coverage rate (you can adjust this)

# Pygame window parameters
window_size = (600, 600)
circle_radius = 10
fence_color = (0, 0, 0)
drone_color = (255, 0, 0)
coverage_color = (0, 0, 255)
background_color = (255, 255, 255)

# Fuzzy logic controller
mutation_rate = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'mutation_rate')
crossover_rate = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'crossover_rate')
efficiency = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'efficiency')

# Define fuzzy sets
mutation_rate.automf(3)
crossover_rate.automf(3)
efficiency.automf(3)

# Define rules
rule1 = ctrl.Rule(mutation_rate['poor'] & crossover_rate['poor'], efficiency['poor'])
rule2 = ctrl.Rule(mutation_rate['average'] & crossover_rate['average'], efficiency['average'])
rule3 = ctrl.Rule(mutation_rate['good'] & crossover_rate['good'], efficiency['good'])

# Create fuzzy system
efficiency_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
efficiency_sim = ctrl.ControlSystemSimulation(efficiency_ctrl)

# Pygame initialization
pygame.init()
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Genetic Algorithm with Fuzzy Logic")

def objective_function(ga_instance, solution, solution_idx):
    # Simulate the area coverage
    covered_area = np.sum(solution)
    efficiency_sim.input['mutation_rate'] = np.random.uniform(0, 1)  # Example, replace with actual values
    efficiency_sim.input['crossover_rate'] = np.random.uniform(0, 1)  # Example, replace with actual values
    efficiency_sim.compute()
    efficiency_value = efficiency_sim.output['efficiency']
    
    # Fitness is a combination of coverage and efficiency
    fitness = (covered_area / total_area) * efficiency_value
    return fitness

# Genetic Algorithm parameters
ga_param = {
    'num_generations': 50,
    'num_parents_mating': 2,
    'mutation_probability': 0.1,
    'crossover_probability': 0.7,
    'sol_per_pop': 8,
    'num_genes': total_area
}

# Create PyGAD optimizer
optimizer = pygad.GA(num_generations=ga_param['num_generations'],
                    num_parents_mating=ga_param['num_parents_mating'],
                    mutation_probability=ga_param['mutation_probability'],
                    crossover_probability=ga_param['crossover_probability'],
                    sol_per_pop=ga_param['sol_per_pop'],
                    num_genes=ga_param['num_genes'],
                    fitness_func=objective_function)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(background_color)

    # Draw the crop plot fence
    pygame.draw.rect(window, fence_color, (50, 50, 500, 500), 2)

    # Run the genetic algorithm
    result = optimizer.run()

    if result is not None:
        solutions, _, _ = result

        # Draw circles based on the solution
        for idx, value in enumerate(solutions[-1]):
            if value == 1:
                pygame.draw.circle(window, coverage_color, (idx % 30 * 20 + 70, idx // 30 * 20 + 70), circle_radius)

        # Draw the drone
        drone_position = (100, 100)
        pygame.draw.circle(window, drone_color, drone_position, circle_radius)

    pygame.display.flip()

pygame.quit()
