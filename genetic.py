from functools import total_ordering
import math
import pandas as pd
import random
import sys
import json

# TESTS = int(sys.argv[3])
# POPULATION_SIZE = int(sys.argv[1])
# GENERATIONS = int(sys.argv[2])
TESTS = 1
POPULATION_SIZE = 100
GENERATIONS = 250
test_data_set = "tag-allocation"

with open("genetic_params.json", "r") as settings_file:
    settings = json.load(settings_file)

show_alloc = False

influence_table_df = pd.read_csv("../" + test_data_set + "/influence_table.csv")
influence_table = influence_table_df.to_numpy()
billboards = pd.read_csv("../" + test_data_set + "/billboards.csv").to_numpy()
meta_df = pd.read_csv("../" + test_data_set + "/meta.csv")
tags_cnt = (meta_df.to_numpy())[0][0]
slots_df = pd.read_csv("../" + test_data_set + "/slots.csv")
slots_cnt = len(slots_df)
slots = slots_df.to_numpy()
budget = (meta_df.to_numpy())[0][1]


# @total_ordering
class Individual:

    def __init__(self, num_slots, alloc=None):
        self.num_slots = num_slots
        if alloc == None:
            self.alloc = random.choices(tags, weights=weights, k=num_slots)
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
        return hasattr(other, "alloc")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.fitness == other.fitness

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.fitness < other.fitness

    def __gt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.fitness > other.fitness

    def __le__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.fitness <= other.fitness

    def __ge__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.fitness >= other.fitness

    def calculate_cost_fitness(self):
        global influence_table
        global budget
        self.cost = 0
        self.fitness = 0
        for assigned_tag_index in range(self.num_slots):
            if self.alloc[assigned_tag_index] == -1:
                continue
            self.cost += influence_table[
                self.alloc[assigned_tag_index] * self.num_slots + assigned_tag_index
            ][4].item()
            self.fitness += influence_table[
                self.alloc[assigned_tag_index] * self.num_slots + assigned_tag_index
            ][1].item()
            if self.cost > budget:
                self.fitness = -1
                break


class Population:

    def __init__(self, population_size, individuals=None):
        global slots_cnt
        self.population_size = population_size
        if individuals == None:
            self.curr_population = [
                Individual(slots_cnt) for i in range(self.population_size)
            ]
        else:
            self.curr_population = individuals
        self.next_population = []
        self.info_history = []
        self.info_dict = {  # might have to add an indec to this when adding to history to ensure that duplicates dont occur, could use sets for it?
            "avg_fitness": -1,
            "max_fitness": -math.inf,
            "min_fitness": math.inf,
            "stdev_fitness": -1,
            "best_alloc": [],
        }  # TODO: add cost stats
        self.update_info()

    def __str__(self):
        if show_alloc:
            return f"avg: {self.info_dict['avg_fitness']:.3f}, max: {self.info_dict['max_fitness']:.3f}, min: {self.info_dict['min_fitness']:.3f}, stdev: {self.info_dict['stdev_fitness']:.3f}, alloc: {self.info_dict['best_alloc']}"
        else:
            return f"avg: {self.info_dict['avg_fitness']:.3f}, max: {self.info_dict['max_fitness']:.3f}, min: {self.info_dict['min_fitness']:.3f}, stdev: {self.info_dict['stdev_fitness']:.3f}"

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
        avg_fitness = total_fitness / self.population_size
        self.info_dict["avg_fitness"] = avg_fitness
        total_deviation = 0
        for indiv in self.curr_population:
            total_deviation += (indiv.fitness - avg_fitness) ** 2
        self.info_dict["stdev_fitness"] = math.sqrt(
            total_deviation / self.population_size
        )
        self.info_dict["best_alloc"] = self[0]
        self.info_history.append(self.info_dict)

    def sortByFitness(indiv):
        return indiv.fitness

    def add_to_next_population(self, indiv_array):
        if len(self.next_population) + len(indiv_array) <= self.population_size:
            self.next_population += indiv_array
        else:
            raise Exception(
                "ERROR: Adding too many individuals to the next generation!"
            )

    def transition_populations(self):
        self.curr_population = self.next_population
        self.next_population = []
        self.info_dict = {
            "avg_fitness": -1,
            "max_fitness": -math.inf,
            "min_fitness": math.inf,
            "stdev_fitness": -1,
            "best_alloc": [],
        }

    def sort(self, sortKey, sortReverse):
        self.curr_population.sort(key=sortKey, reverse=sortReverse)

    def print_history(self):
        for log_index in range(len(self.info_history)):
            if show_alloc:
                history_line = f"max: {self.info_history[log_index]['max_fitness']:.3f}, avg: {self.info_history[log_index]['avg_fitness']:.3f}, min: {self.info_history[log_index]['min_fitness']:.3f}, stdev: {self.info_history[log_index]['stdev_fitness']:.3f}, alloc: {self.info_history[log_index]['best_alloc']}"
                print(history_line)
                output_file.write(
                    f"{log_index},{self.info_history[log_index]['max_fitness']:.3f},{self.info_history[log_index]['avg_fitness']:.3f},{self.info_history[log_index]['min_fitness']:.3f},{self.info_history[log_index]['stdev_fitness']:.3f},{self.info_history[log_index]['best_alloc']}\n"
                )
            else:
                history_line = f"max: {self.info_history[log_index]['max_fitness']:.3f}, avg: {self.info_history[log_index]['avg_fitness']:.3f}, min: {self.info_history[log_index]['min_fitness']:.3f}, stdev: {self.info_history[log_index]['stdev_fitness']:.3f}"
                print(history_line)
                output_file.write(
                    f"{log_index},{self.info_history[log_index]['max_fitness']:.3f},{self.info_history[log_index]['avg_fitness']:.3f},{self.info_history[log_index]['min_fitness']:.3f},{self.info_history[log_index]['stdev_fitness']:.3f}\n"
                )


# === === === GENERATION STAGE === === ===

population_size = POPULATION_SIZE
tags = [-1] + [i for i in range(tags_cnt)]
# heavily weight on no allocation as to not overload budget
average_slot_cost = (
    sum(billboards[i][2] for i in (slots[j][1] for j in range(slots_cnt))) / slots_cnt
)
# the closer the average cost is to the budget, increase odds for unassigned
# if avgcost == budget, then -1 should be weighted such that it most likely will assign only one slot
weights = [(average_slot_cost / budget) * (slots_cnt * tags_cnt - tags_cnt)] + [
    1 for i in range(tags_cnt)
]

population = Population(population_size)

print("=== INITIAL POPULATION ===")
for i in range(population_size):
    print(population[i])
print(population)

initial_populations = [
    [
        Population(
            population_size,
            [
                Individual(slots_cnt, indiv.alloc)
                for indiv in population.curr_population
            ],
        )
        for _ in range(TESTS)
    ]
    for _ in range(len(settings))
]

output_summary = open("output_B_summary.csv", "w")
output_summary.write("index,test_no,test_name,max,avg,min,stdev\n")

total_cost = 0
total_influence = 0

for config_i in range(len(settings)):
    if not settings[config_i]["test?"]:
        continue
    print(f"current config: {settings[config_i]['name']}")
    for test_i in range(TESTS):
        working_population = initial_populations[config_i][test_i]
        output_file = open(
            "output_B_"
            + settings[config_i]["name"]
            + "_"
            + str(POPULATION_SIZE)
            + "_"
            + str(GENERATIONS)
            + "_"
            + str(test_i)
            + ".csv",
            "w",
        )
        # output_file = open("test_output.txt", "w")
        output_file.write("generation,max,avg,min,stdev\n")
        # for i in settings:
        #     output_file.write(f"{i}: {settings[i]}\n")

        # population = [random.choices(tags, weights = weights, k = slots_cnt) for i in range(population_size)]
        # population_cost = [0 for i in range(population_size)]
        # population_fitness = [0 for i in range(population_size)]

        # == calculate fitness ==
        # for allocIndex in range(population_size):
        #     population_info[allocIndex].calculate_cost_fitness()

        for i in range(GENERATIONS):

            # === === === SELECTION STAGE === === ===

            parents = []
            parent_child_ratio = settings[config_i]["parent_child_ratio"]
            num_parents = math.ceil(population_size * parent_child_ratio)
            num_children = population_size - num_parents

            # > Roulette Wheel Selection
            # - use random.choices to weight each alloc by their fitness
            RWS_percentage = settings[config_i]["RWS_percentage"]
            num_RWS_wins = math.ceil(num_parents * RWS_percentage)
            RWS_weights = [
                working_population[allocIndex].fitness + 1
                for allocIndex in range(population_size)
            ]
            if not (sum(RWS_weights) > 0):
                RWS_weights = [
                    1 for _ in range(population_size)
                ]  # give every alloc an equal weight if every alloc is over budget
            RWS_wins = random.choices(
                working_population, weights=RWS_weights, k=num_RWS_wins
            )

            # > Tournament Selection
            TS_percentage = 1.0 - RWS_percentage
            num_TS_wins = num_parents - num_RWS_wins
            TS_wins = []
            # tournament_size = math.ceil(population_size / 4) # could be a parameter
            tournament_size = random.randint(1, population_size)  # could be a parameter
            tournament = []
            for _ in range(num_TS_wins):
                tournament = random.choices(working_population, k=tournament_size)
                TS_wins += [max(tournament)]

            parents += RWS_wins
            parents += TS_wins
            working_population.add_to_next_population(RWS_wins)
            working_population.add_to_next_population(TS_wins)

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
            NPC_percentage = settings[config_i]["NPC_percentage"]
            NPC_children = []
            num_NPC_children = math.ceil(num_children * NPC_percentage)
            for _ in range(num_NPC_children):
                parent_1 = random.choice(parents)
                parent_2 = random.choice(parents)
                num_crossover_points = random.choices(
                    range(1, slots_cnt - 1),
                    weights=[
                        1 for _ in range(1, slots_cnt - 1)
                    ],  # added weights just in case this needs to be adjusted
                    k=1,
                )[0]
                crossover_points = random.sample(
                    range(1, slots_cnt), k=num_crossover_points
                )
                crossover_points.sort()
                # for i in range(num_crossover_points):
                #     if len(crossover_points) == 0:
                #         crossover_points += [random.choice(range(1, slots_cnt-(num_crossover_points-1)))]
                #     else:
                #         crossover_points += [random.choice(range(crossover_points[i-1]+1, slots_cnt-(num_crossover_points-len(crossover_points))+1))]
                alloc = [
                    (parent_1 if c % 2 == 0 else parent_2).alloc[
                        (0 if c == 0 else crossover_points[c - 1]) : (
                            slots_cnt
                            if c == len(crossover_points)
                            else crossover_points[c]
                        )
                    ]
                    for c in range(len(crossover_points) + 1)
                ]
                child = Individual(slots_cnt, sum(alloc, []))
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
                        (
                            parent_1.alloc[i]
                            if random.random() <= 0.5
                            else parent_2.alloc[i]
                        )
                        for i in range(slots_cnt)
                    ],
                )
                UC_children.append(child)

            working_population.add_to_next_population(NPC_children)
            working_population.add_to_next_population(UC_children)

            # === === === MUTATION STAGE === === ===

            working_population.transition_populations()

            mutation_probability = settings[config_i]["mutation_probability"]

            for indiv in working_population.curr_population:
                mutation_check = random.random()
                if mutation_check <= mutation_probability:
                    # print("mutation time!")
                    mutant = indiv
                    # initial_fitness = mutant.fitness
                    mutation_index = random.randint(0, slots_cnt - 1)
                    mutant.alloc[mutation_index] = random.choice(tags)
                    mutant.calculate_cost_fitness()
                    # new_fitness = mutant.fitness
                    # print(f"after: {mutant}, diff: {new_fitness-initial_fitness}")

            working_population.update_info()

        # print(" === population === ")
        # print(population)
        # print(" === population_cost === ")
        # print(population_cost)
        # print(" === population_fitness === ")
        # print(population_fitness)
        def sortByFitness(indiv):
            return indiv.fitness

        working_population.sort(sortByFitness, True)

        # print(f"=== POPULATION AFTER {GENERATIONS} GENERATIONS ===")
        # for i in range(working_population.population_size):
        #     print(working_population[i])
        # print(working_population)

        # print("=== POPULATION HISTORY ===")
        # working_population.print_history()

        # print("=== RWS WINS ===")
        # for i in range(len(RWS_wins)):
        #     print(RWS_wins[i])

        # print("=== CHILDREN ===")
        # for i in range(len(OPC_children)):
        #     print(OPC_children[i])

        output_file.close()
        last_gen_info = working_population.info_dict
        output_summary.write(
            f"{config_i+test_i},\"{settings[config_i]['name']}\",{test_i},{last_gen_info['max_fitness']},{last_gen_info['avg_fitness']},{last_gen_info['min_fitness']},{last_gen_info['stdev_fitness']}\n"
        )

        # comparisons
        total_cost = working_population[0].cost
        total_influence = working_population[0].fitness
output_summary.close()
