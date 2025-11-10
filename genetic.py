from functools import total_ordering
import math
import pandas as pd
import random
import sys
import json

TESTS = int(sys.argv[2])
GENERATIONS = int(sys.argv[1])
test_data_set = "test_data_big"

with open("genetic_params.json", "r") as settings_file:
    settings = json.load(settings_file)
print(settings)

show_alloc = settings["show_alloc"]

influence_table_df = pd.read_csv("../"+test_data_set+"/influence_table.csv")
influence_table = influence_table_df.to_numpy()
billboards = pd.read_csv("../"+test_data_set+"/billboards.csv").to_numpy()
meta_df = pd.read_csv("../"+test_data_set+"/meta.csv")
tags_cnt = (meta_df.to_numpy())[0][0]
slots_df = pd.read_csv("../"+test_data_set+"/slots.csv")
slots_cnt = len(slots_df)
slots = slots_df.to_numpy()
budget = (meta_df.to_numpy())[0][1]

# @total_ordering
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
        if show_alloc:
            return f"{{'alloc': {self.alloc}, 'cost': {self.cost}, 'fitness': {self.fitness}}}"
        else:
            return f"{{'cost': {self.cost}, 'fitness': {self.fitness}}}"
    
    def _is_valid_operand(self, other):
        return (hasattr(other, "alloc"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.fitness == other.fitness)
    
    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.fitness < other.fitness)
    def __gt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.fitness > other.fitness)
    def __le__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.fitness <= other.fitness)
    def __ge__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.fitness >= other.fitness)

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

class Population:

    def __init__(self, population_size):
        global slots_cnt
        self.population_size = population_size
        self.curr_population = [
            Individual(slots_cnt) for i in range(self.population_size)
        ]
        self.next_population = []
        self.info_history = []
        self.info_dict = { # might have to add an indec to this when adding to history to ensure that duplicates dont occur, could use sets for it?
            "avg_fitness": -1,
            "max_fitness": -math.inf,
            "min_fitness": math.inf,
            "stdev_fitness": -1,
            "best_alloc": []
        } # TODO: add cost stats
        self.update_info()

    def __str__(self):
        if show_alloc:
            return f"avg: {self.info_dict["avg_fitness"]:.3f}, max: {self.info_dict["max_fitness"]:.3f}, min: {self.info_dict["min_fitness"]:.3f}, stdev: {self.info_dict["stdev_fitness"]:.3f}, alloc: {self.info_dict["best_alloc"]}"
        else:
            return f"avg: {self.info_dict["avg_fitness"]:.3f}, max: {self.info_dict["max_fitness"]:.3f}, min: {self.info_dict["min_fitness"]:.3f}, stdev: {self.info_dict["stdev_fitness"]:.3f}"

    def __getitem__(self, index):
        return self.curr_population[index]
    
    def __len__(self):
        return self.population_size
    
    def update_info(self):
        total_fitness = 0
        for indiv in self.curr_population:
            total_fitness += indiv.fitness
            if indiv.fitness > self.info_dict["max_fitness"]:
                self.info_dict["max_fitness"] = indiv.fitness
            if indiv.fitness < self.info_dict["min_fitness"] and indiv.fitness != -1:
                self.info_dict["min_fitness"] = indiv.fitness
        avg_fitness = total_fitness/self.population_size
        self.info_dict["avg_fitness"] = avg_fitness
        total_deviation = 0
        for indiv in self.curr_population:
            total_deviation += (indiv.fitness - avg_fitness) ** 2
        self.info_dict["stdev_fitness"] = math.sqrt(total_deviation/self.population_size)
        self.info_dict["best_alloc"] = self[0]
        self.info_history.append(self.info_dict)
    
    def sortByFitness(indiv):
        return indiv.fitness

    def add_to_next_population(self, indiv_array):
        if len(self.next_population) + len(indiv_array) <= self.population_size:
            self.next_population += indiv_array
        else:
            raise Exception("ERROR: Adding too many individuals to the next generation!")
    
    def transition_populations(self):
        self.curr_population = self.next_population
        self.next_population = []
        self.info_dict = { 
            "avg_fitness": -1,
            "max_fitness": -math.inf,
            "min_fitness": math.inf,
            "stdev_fitness": -1,
            "best_alloc": []
        }

    def sort(self, sortKey, sortReverse):
        self.curr_population.sort(key=sortKey, reverse=sortReverse)

    def print_history(self):
        for log_index in range(len(self.info_history)):
            if show_alloc:
                history_line = f"max: {self.info_history[log_index]["max_fitness"]:.3f}, avg: {self.info_history[log_index]["avg_fitness"]:.3f}, min: {self.info_history[log_index]["min_fitness"]:.3f}, stdev: {self.info_history[log_index]["stdev_fitness"]:.3f}, alloc: {self.info_history[log_index]["best_alloc"]}"
                print(history_line)
                output_file.write(f"{log_index},{self.info_history[log_index]["max_fitness"]:.3f},{self.info_history[log_index]["avg_fitness"]:.3f},{self.info_history[log_index]["min_fitness"]:.3f},{self.info_history[log_index]["stdev_fitness"]:.3f},{self.info_history[log_index]["best_alloc"]}\n")
            else:
                history_line = f"max: {self.info_history[log_index]["max_fitness"]:.3f}, avg: {self.info_history[log_index]["avg_fitness"]:.3f}, min: {self.info_history[log_index]["min_fitness"]:.3f}, stdev: {self.info_history[log_index]["stdev_fitness"]:.3f}"
                print(history_line)
                output_file.write(f"{log_index},{self.info_history[log_index]["max_fitness"]:.3f},{self.info_history[log_index]["avg_fitness"]:.3f},{self.info_history[log_index]["min_fitness"]:.3f},{self.info_history[log_index]["stdev_fitness"]:.3f}\n")

for test_i in range(TESTS):
    output_file = open("output_B_mutation1_"+sys.argv[1]+"_"+str(test_i)+".csv", "w")
    # output_file = open("test_output.txt", "w")
    output_file.write("generation,max,avg,min,stdev\n")
    # for i in settings:
    #     output_file.write(f"{i}: {settings[i]}\n")

    # === === === GENERATION STAGE === === ===

    population_size = settings["population_size"]
    tags = [-1] + [i for i in range(tags_cnt)]
    # heavily weight on no allocation as to not overload budget
    average_slot_cost = sum(billboards[i][2] for i in (slots[j][1] for j in range(slots_cnt)))/slots_cnt
    # the closer the average cost is to the budget, increase odds for unassigned
    # if avgcost == budget, then -1 should be weighted such that it most likely will assign only one guy
    weights = [(average_slot_cost/budget)*(slots_cnt*tags_cnt - tags_cnt)] + [1 for i in range(tags_cnt)]

    population = Population(population_size)

    print("=== INITIAL POPULATION ===")
    for i in range(population_size):
        print(population[i])
    print(population)

    # population = [random.choices(tags, weights = weights, k = slots_cnt) for i in range(population_size)]
    # population_cost = [0 for i in range(population_size)]
    # population_fitness = [0 for i in range(population_size)]

    # == calculate fitness ==
    # for allocIndex in range(population_size):
    #     population_info[allocIndex].calculate_cost_fitness()

    for i in range(GENERATIONS):

        # === === === SELECTION STAGE === === ===

        parents = []
        parent_child_ratio = settings["parent_child_ratio"]
        num_parents = math.ceil(population_size * parent_child_ratio)
        num_children = population_size - num_parents

        # > Roulette Wheel Selection
        # - use random.choices to weight each alloc by their fitness
        RWS_percentage = settings["RWS_percentage"]
        num_RWS_wins = math.ceil(num_parents * RWS_percentage)
        RWS_wins = random.choices(
            population,
            weights = [population[allocIndex].fitness+1 for allocIndex in range(population_size)],
            k = num_RWS_wins
        )

        # > Tournament Selection
        TS_percentage = 1.0 - RWS_percentage
        num_TS_wins = num_parents - num_RWS_wins
        TS_wins = []
        tournament_size = math.ceil(population_size / 4)
        tournament = []
        for _ in range(num_TS_wins):
            tournament = random.choices(
                population,
                k = tournament_size
            )
            TS_wins += [max(tournament)]

        parents += RWS_wins
        parents += TS_wins
        population.add_to_next_population(RWS_wins)
        population.add_to_next_population(TS_wins)

        # === === === CROSSOVER STAGE === === ===

        # // currently not using this probability to satisfy population size
        # crossover_probability = 0.5

        # > One-Point Crossover
        OPC_children = []
        # for parent_1 in parents:
        #     parent_2 = random.choice(parents)
        #     crossover_point = random.choice(range(1, slots_cnt-1))
        #     child = Individual(
        #         slots_cnt,
        #         parent_1.alloc[0:crossover_point] +
        #         parent_2.alloc[crossover_point:slots_cnt]
        #     )
        #     OPC_children.append(child)

        # > Two-Point Crossover
        # TPC_children = []
        # for parent_1 in parents:
        #     parent_2 = random.choice(parents)
        #     crossover_points = []
        #     crossover_points += [random.choice(range(1, slots_cnt-1))]    
        #     crossover_points += [random.choice(range(crossover_points[0]+1, slots_cnt-1))]   
        #     child = Individual(
        #         slots_cnt,
        #         parent_1.alloc[0:crossover_points[0]] +
        #         parent_2.alloc[crossover_points[0]:crossover_points[1]] +
        #         parent_1.alloc[crossover_points[1]:slots_cnt]
        #     )

        # > N-Point Crossover
        NPC_percentage = settings["NPC_percentage"]
        NPC_children = []
        num_NPC_children = math.ceil(num_children*NPC_percentage)
        for _ in range(num_NPC_children):
            parent_1 = random.choice(parents)
            parent_2 = random.choice(parents)
            num_crossover_points = random.choices(
                range(1, slots_cnt-1),
                weights = [1 for _ in range(1, slots_cnt-1)], # added weights just in case this needs to be adjusted
                k = 1
            )[0]
            crossover_points = random.sample(range(1, slots_cnt), k=num_crossover_points)
            crossover_points.sort()
            # for i in range(num_crossover_points):
            #     if len(crossover_points) == 0:
            #         crossover_points += [random.choice(range(1, slots_cnt-(num_crossover_points-1)))]
            #     else:
            #         crossover_points += [random.choice(range(crossover_points[i-1]+1, slots_cnt-(num_crossover_points-len(crossover_points))+1))]
            alloc = [
                    (parent_1 if c%2==0 else parent_2).alloc[
                        (0 if c==0 else crossover_points[c-1]):
                        (slots_cnt if c==len(crossover_points) else crossover_points[c])
                        ]
                    for c in range(len(crossover_points)+1)
                ]
            child = Individual(
                slots_cnt,
                sum(alloc, [])
            )
            NPC_children.append(child)

        # > Uniform Crossover
        UC_percentage = 1.0 - NPC_percentage
        UC_children = []
        num_UC_children = num_children - num_NPC_children
        for _ in range(num_UC_children):
            parent_1 = random.choice(parents)
            parent_2 = random.choice(parents)
            child = Individual(
                slots_cnt,
                [
                    (parent_1.alloc[i] if random.random() <= 0.5 else parent_2.alloc[i])
                    for i in range(slots_cnt)
                ]
            )
            UC_children.append(child)

        population.add_to_next_population(NPC_children)
        population.add_to_next_population(UC_children)

        # === === === MUTATION STAGE === === ===

        population.transition_populations()

        mutation_probability = settings["mutation_probability"]

        for indiv in population:
            if random.random() <= mutation_probability:
                # print("mutation time!")
                mutant = random.choice(population.curr_population)
                # initial_fitness = mutant.fitness
                mutation_index = random.randint(0, slots_cnt-1)
                mutant.alloc[mutation_index] = random.choice(tags)
                mutant.calculate_cost_fitness()
                # new_fitness = mutant.fitness
                # print(f"after: {mutant}, diff: {new_fitness-initial_fitness}")
        
        population.update_info()

    # print(" === population === ")
    # print(population)
    # print(" === population_cost === ")
    # print(population_cost)
    # print(" === population_fitness === ")
    # print(population_fitness)
    def sortByFitness(indiv):
        return indiv.fitness

    population.sort(sortByFitness, True)

    print(f"=== POPULATION AFTER {GENERATIONS} GENERATIONS ===")
    for i in range(population.population_size):
        print(population[i])
    print(population)

    print("=== POPULATION HISTORY ===")
    population.print_history()

    # print("=== RWS WINS ===")
    # for i in range(len(RWS_wins)):
    #     print(RWS_wins[i])

    # print("=== CHILDREN ===")
    # for i in range(len(OPC_children)):
    #     print(OPC_children[i])
    
    output_file.close()