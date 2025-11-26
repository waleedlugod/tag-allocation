import matplotlib.pyplot as plt
import numpy as np

output = open("output.txt", "r")

HEURISTICS_CNT = 4

performances = []
avg_approx_ratios = []
avg_costs = []

for _ in range(HEURISTICS_CNT):
    performances.append(float(output.readline().split(" ")[-1]))
    avg_approx_ratios.append(float(output.readline().split(" ")[-1]))
    avg_costs.append(float(output.readline().split(" ")[-1]))

x = np.arange(HEURISTICS_CNT)
width = 0.2

# performance and approximation ratio
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

# average costs
# plt.figure()
# plt.bar(x, avg_costs, width, color="orange")
# plt.xticks(x, ["Greedy (Influence)", "Greedy (Cost)", "Greedy (Influence/Cost)"])
# plt.xlabel("Heuristics")
# plt.ylabel("Avg Cost")
# plt.title("Average Costs of Greedys")
# axes = plt.gca()
# axes.set_ylim([0, brute_avg_cost])

# influence distribution
# note: graph is right skewed as not all users contribute to the final influence value (i.e. 0 value)
influences = open("influences.txt", "r").read().splitlines()
influences = [float(_) for _ in influences if "\x00" not in _ and _ != "" and "." in _]
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
