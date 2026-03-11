import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

output = open("output.txt", "r")

HEURISTICS_CNT = 4
SHOW_METRICS_GRAPHS = True
SHOW_INFLUENCE_GRAPHS = True

settings = pd.read_csv("settings.csv").to_numpy()[0]
(
    NUM_TEST_CASES,
    slots_start,
    slots_step,
    slots_steps,
    budget_start,
    budget_step,
    budget_steps,
) = settings
performances = []
avg_approx_ratios = []
avg_costs = []
metrics = {
    # "Brute-force"
    "DP": {},
    "Greedy (Influence)": {},
    "Greedy (Cost)": {},
    "Greedy (Influence/Cost)": {},
    "Genetic (100 population, 250 generations, Default Config)": {},
}


# setup
for h in metrics:
    metrics[h]["inc_slots"] = []
    metrics[h]["inc_budget"] = []


# read metrics
for _ in range(HEURISTICS_CNT):
    performances.append(float(output.readline().split(" ")[-1]))
    avg_approx_ratios.append(float(output.readline().split(" ")[-1]))
    avg_costs.append(float(output.readline().split(" ")[-1]))

# read computation times
while True:
    line = output.readline().strip()
    if line == "":
        break
    inputs = line.split(",")
    slots = int(inputs[0].split(" ")[-1])
    budget = int(inputs[1].split(" ")[-1])
    for h in range(HEURISTICS_CNT + 1):
        line = output.readline().strip().split(" ")
        comp_time = float(line[2])
        heuristic_title = " ".join(line[4:])
        if budget == budget_start:
            metrics[heuristic_title]["inc_slots"].append(comp_time)
        if slots == slots_start:
            metrics[heuristic_title]["inc_budget"].append(comp_time)


x = np.arange(HEURISTICS_CNT)
width = 0.2

if SHOW_METRICS_GRAPHS:
    ### performance and approximation ratio
    plt.figure(figsize=(8, 8))
    plt.bar(x - width, performances, width, color="green")
    plt.bar(x, avg_approx_ratios, width, color="orange")
    plt.bar(x + width, avg_costs, width, color="red")
    plt.xticks(
        x,
        ["Greedy (Influence)", "Greedy (Cost)", "Greedy (Influence/Cost)", "Genetic"],
    )
    plt.xlabel("Heuristics")
    plt.ylabel("Ratio to Optimal")
    plt.legend(
        ["Performance", "Avg Approximation Ratio", "Avg Cost Approximation Ratio"],
        loc="lower right",
    )
    plt.title("Correctness and Approximation Ratios of Greedys")

    ### average costs
    # plt.figure()
    # plt.bar(x, avg_costs, width, color="orange")
    # plt.xticks(x, ["Greedy (Influence)", "Greedy (Cost)", "Greedy (Influence/Cost)"])
    # plt.xlabel("Heuristics")
    # plt.ylabel("Avg Cost")
    # plt.title("Average Costs of Greedys")
    # axes = plt.gca()
    # axes.set_ylim([0, brute_avg_cost])

    ### increasing slots
    plt.figure()
    y = np.arange(slots_start, slots_start + slots_step * slots_steps, slots_step)
    plt.plot(
        y,
        metrics["DP"]["inc_slots"],
        "purple",
        y,
        metrics["Greedy (Cost)"]["inc_slots"],
        "green",
        y,
        metrics["Greedy (Influence)"]["inc_slots"],
        "orange",
        y,
        metrics["Greedy (Influence/Cost)"]["inc_slots"],
        "red",
        y,
        metrics["Genetic (100 population, 250 generations, Default Config)"][
            "inc_slots"
        ],
        "yellow",
    )
    plt.legend(
        [
            "DP",
            "Greedy (Cost)",
            "Greedy (Influence)",
            "Greedy (Influence/Cost)",
            "Genetic (100 population, 250 generations, Default Config)",
        ]
    )
    plt.xlabel("Slot count")
    plt.ylabel("Computation time (seconds)")

    ### increasing budget
    plt.figure()
    y = np.arange(budget_start, budget_start + budget_step * budget_steps, budget_step)
    plt.plot(
        y,
        metrics["DP"]["inc_budget"],
        "purple",
        y,
        metrics["Greedy (Cost)"]["inc_budget"],
        "green",
        y,
        metrics["Greedy (Influence)"]["inc_budget"],
        "orange",
        y,
        metrics["Greedy (Influence/Cost)"]["inc_budget"],
        "red",
        y,
        metrics["Genetic (100 population, 250 generations, Default Config)"][
            "inc_budget"
        ],
        "yellow",
    )
    plt.legend(
        [
            "DP",
            "Greedy (Cost)",
            "Greedy (Influence)",
            "Greedy (Influence/Cost)",
            "Genetic (100 population, 250 generations, Default Config)",
        ]
    )
    plt.xlabel("Budget")
    plt.ylabel("Computation time (seconds)")


if SHOW_INFLUENCE_GRAPHS:
    # influence distribution
    # note: graph is right skewed as not all users contribute to the final influence value (i.e. 0 value)
    influences = open("influences.txt", "r").read().splitlines()
    influences = [
        float(_) for _ in influences if "\x00" not in _ and _ != "" and "." in _
    ]
    plt.figure()
    plt.hist(influences, rwidth=0.9)
    plt.xlabel("Influence")
    plt.ylabel("Count")
    plt.title("Distribution of Influence Values From Influence Table")

    raw_influences = open("raw_influences.txt", "r").read().splitlines()
    raw_influences = [
        float(_) for _ in raw_influences if "\x00" not in _ and _ != "" and "." in _
    ]
    plt.figure()
    plt.hist(raw_influences, rwidth=0.9)
    plt.xlabel("Influence")
    plt.ylabel("Count")
    plt.title("Distribution of Population Influence Values")

    # influence distribution (all test cases)
    # note: graph is right skewed as not all users contribute to the final influence value (i.e. 0 value)
    influences_all = open("influences_all.txt", "r").read().splitlines()
    influences_all = [
        float(_) for _ in influences_all if "\x00" not in _ and _ != "" and "." in _
    ]
    plt.figure()
    plt.hist(influences_all, rwidth=0.9)
    plt.xlabel("Influence")
    plt.ylabel("Count")
    plt.title("Distribution of Influence Values From Influence Table (All Tests)")

    raw_influences_all = open("raw_influences_all.txt", "r").read().splitlines()
    raw_influences_all = [
        float(_) for _ in raw_influences_all if "\x00" not in _ and _ != "" and "." in _
    ]
    mean = np.mean(raw_influences_all)
    std = np.std(raw_influences_all)
    plt.figure()
    plt.hist(raw_influences_all, rwidth=0.9)
    plt.xlabel("Influence")
    plt.ylabel("Count")
    plt.title("Distribution of Population Influence Values (All Tests)")

plt.show()
