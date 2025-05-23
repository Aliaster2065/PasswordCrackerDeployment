import streamlit as st
import random
import time

# Constants
POP_SIZE = 500
MUTATION_RATE = 0.1
ALLOWED_CHARS = ' abcdefghijklmnopqrstuvwxyz0123456789'

# Streamlit UI
st.title("Password Cracker 🔐")
password_input = st.text_input("Enter the password to crack:")

if st.button("Crack Password"):
    if not password_input:
        st.warning("Please enter a password first.")
    else:
        # Genetic algorithm
        def initialize_population(password):
            return [[random.choice(ALLOWED_CHARS) for _ in range(len(password))] for _ in range(POP_SIZE)]

        def fitness(individual, password):
            mismatches = sum(1 for a, b in zip(individual, password) if a != b)
            return [individual, mismatches]

        def selection(population):
            return sorted(population, key=lambda x: x[1])[:int(POP_SIZE * 0.5)]

        def crossover(parents, chromo_length):
            offspring = []
            for _ in range(POP_SIZE):
                parent1 = random.choice(parents)[0]
                parent2 = random.choice(parents)[0]
                cross_point = random.randint(1, chromo_length - 1)
                child = parent1[:cross_point] + parent2[cross_point:]
                offspring.append(child)
            return offspring

        def mutate(offspring):
            for individual in offspring:
                for i in range(len(individual)):
                    if random.random() < MUTATION_RATE:
                        individual[i] = random.choice(ALLOWED_CHARS)
            return offspring

        def crack_password(password):
            generation = 1
            population = initialize_population(password)
            scored_population = [fitness(indiv, password) for indiv in population]
            start_time = time.time()

            while True:
                scored_population.sort(key=lambda x: x[1])
                best_match = scored_population[0]

                st.write(f"Generation {generation} | Best Match: {''.join(best_match[0])} | Fitness: {best_match[1]}")
                if best_match[1] == 0:
                    end_time = time.time()
                    st.success(f"🎉 Password cracked: {''.join(best_match[0])}")
                    st.info(f"✅ Cracked in generation {generation}")
                    st.info(f"⏱️ Time taken: {round(end_time - start_time, 2)} seconds")
                    break

                selected = selection(scored_population)
                offspring = crossover(selected, len(password))
                mutated = mutate(offspring)
                scored_population = [fitness(indiv, password) for indiv in mutated]
                generation += 1

        crack_password(password_input)

        