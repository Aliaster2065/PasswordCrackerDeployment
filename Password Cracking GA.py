import random

# Constants
POP_SIZE = 500
MUTATION_RATE = 0.1
PASSWORD = 'theslugcat092'
ALLOWED_CHARS = ' abcdefghijklmnopqrstuvwxyz0123456789'

def initialize_population(password):
    population = []
    length = len(password)
    for _ in range(POP_SIZE):
        individual = [random.choice(ALLOWED_CHARS) for _ in range(length)]
        population.append(individual)
    return population

def fitness(individual, password):
    # Fitness is based on how many characters are different
    mismatches = sum(1 for a, b in zip(individual, password) if a != b)
    return [individual, mismatches]

def selection(population):
    sorted_population = sorted(population, key=lambda x: x[1])
    return sorted_population[:int(POP_SIZE * 0.5)]

def crossover(parents, chromo_length, population):
    offspring = []
    for _ in range(POP_SIZE):
        parent1 = random.choice(parents)[0]
        parent2 = random.choice(population[:int(POP_SIZE * 0.5)])[0]
        cross_point = random.randint(1, chromo_length - 1)
        child = parent1[:cross_point] + parent2[cross_point:]
        offspring.append(child)
    return offspring

def mutate(offspring):
    mutated = []
    for individual in offspring:
        for i in range(len(individual)):
            if random.random() < MUTATION_RATE:
                individual[i] = random.choice(ALLOWED_CHARS)
        mutated.append(individual)
    return mutated

def replace(old_population, new_generation):
    for i in range(len(old_population)):
        if old_population[i][1] > new_generation[i][1]:
            old_population[i] = new_generation[i]
    return old_population

def genetic_password_crack():
    population = initialize_population(PASSWORD)
    generation = 1
    scored_population = [fitness(indiv, PASSWORD) for indiv in population]

    while True:
        scored_population = sorted(scored_population, key=lambda x: x[1])
        best_match = scored_population[0]

        print(f"Generation {generation} | Best Match: {''.join(best_match[0])} | Fitness: {best_match[1]}")

        if best_match[1] == 0:
            print(f"\n🔐 Password successfully cracked in generation {generation}!")
            print(f"Password: {''.join(best_match[0])}")
            break

        selected = selection(scored_population)
        crossed = crossover(selected, len(PASSWORD), scored_population)
        mutated = mutate(crossed)
        new_generation = [fitness(indiv, PASSWORD) for indiv in mutated]
        scored_population = replace(scored_population, new_generation)

        generation += 1

# Run the simulation
genetic_password_crack()