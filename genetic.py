import pandas as pd
import random

GENERATIONS = 25

influence_table_df = pd.read_csv("influence_table.csv")
influence_table = influence_table_df.to_numpy()
meta_df = pd.read_csv("meta.csv")
tags_cnt = (meta_df.to_numpy())[0][0]
slots_df = pd.read_csv("slots.csv")
slots_cnt = len(slots_df)
budget = (meta_df.to_numpy())[0][1]

class Individual:

    def __init__(self, num_slots, alloc = None):
        self.num_slots = num_slots
        if alloc == None:
            self.alloc = random.choices(tags, weights = weights, k = num_slots)
        else:
            self.alloc = alloc
        self.cost = 0
        self.fitness = 0
        self.calculate_cost_fitness()

    def __str__(self):
        return f"{{'alloc': {self.alloc}, 'cost': {self.cost}, 'fitness': {self.fitness}}}"
    
    def calculate_cost_fitness(self):
        global influence_table
        global budget
        self.cost = 0
        self.fitness = 0
        for assigned_tag_index in range(self.num_slots):
            if self.alloc[assigned_tag_index] == -1:
                continue
            self.cost += influence_table[self.alloc[assigned_tag_index]*self.num_slots+assigned_tag_index][4].item()
            self.fitness += influence_table[self.alloc[assigned_tag_index]*self.num_slots+assigned_tag_index][1].item()
            if self.cost > budget:
                self.fitness = -1
                break


# == generate initial population ==
population_size = 100
tags = [-1] + [i for i in range(tags_cnt)]
# heavily weight on no allocation as to not overload budget
weights = [tags_cnt*2] + [1 for i in range(tags_cnt)]

population = [
    Individual(slots_cnt) for i in range(population_size)
]

print("=== INITIAL POPULATION ===")
for i in range(population_size):
    print(population[i])

# population = [random.choices(tags, weights = weights, k = slots_cnt) for i in range(population_size)]
# population_cost = [0 for i in range(population_size)]
# population_fitness = [0 for i in range(population_size)]

# == calculate fitness ==
# for allocIndex in range(population_size):
#     population_info[allocIndex].calculate_cost_fitness()

for i in range(GENERATIONS):

    # == selection process ==

    parent_child_ratio = 0.5

    next_generation = []

    # > Roulette Wheel Selection
    # - use random.choices to weight each alloc by their fitness
    RWS_percentage = 1.0
    RWS_wins = random.choices(
        population,
        weights = [population[allocIndex].fitness for allocIndex in range(population_size)],
        k = int(population_size*RWS_percentage*parent_child_ratio) # TODO: adjust for fractional values
    )

    next_generation += RWS_wins

    # > Tournament Selection

    # == crossover step ==

    crossover_probability = 0.5


    # > One-Point Crossover
    OPC_children = []
    for parent in RWS_wins:
        other_parent = random.choice(RWS_wins)
        crossover_point = random.choice(range(slots_cnt-1))+1
        child = Individual(slots_cnt, parent.alloc[0:crossover_point] + other_parent.alloc[crossover_point:slots_cnt])
        OPC_children.append(child)

    next_generation += OPC_children

    # == mutation step ==

    population = next_generation


# print(" === population === ")
# print(population)
# print(" === population_cost === ")
# print(population_cost)
# print(" === population_fitness === ")
# print(population_fitness)
def sortByFitness(indiv):
    return indiv.fitness

population.sort(key=sortByFitness, reverse=True)

print(f"=== POPULATION AFTER {GENERATIONS} GENERATIONS ===")
for i in range(population_size):
    print(population[i])

# print("=== RWS WINS ===")
# for i in range(len(RWS_wins)):
#     print(RWS_wins[i])

# print("=== CHILDREN ===")
# for i in range(len(OPC_children)):
#     print(OPC_children[i])