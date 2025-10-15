import matplotlib.pyplot as plt
import numpy as np

output = open("output.txt", "r")

HEURISTICS_CNT = 4

performances = []
avg_approx_ratios = []
avg_costs = []

brute_avg_cost = float(output.readline().split(" ")[-1])
for _ in range(HEURISTICS_CNT - 1):
    performances.append(float(output.readline().split(" ")[-1]))
    avg_approx_ratios.append(float(output.readline().split(" ")[-1]))
    avg_costs.append(float(output.readline().split(" ")[-1]))


x = np.arange(HEURISTICS_CNT - 1)
width = 0.35

# performance and approximation ratio
plt.figure()
plt.bar(x - width, performances, width, color="green")
plt.bar(x, avg_approx_ratios, width, color="orange")
plt.xticks(x, ["Greedy (Influence)", "Greedy (Cost)", "Greedy (Influence/Cost)"])
plt.xlabel("Heuristics")
plt.ylabel("Percent")
plt.legend(["Performance", "Avg Approximation Ratio"])
plt.title("Correctness and Approximation Ratios of Greedys")

# average costs
plt.figure()
plt.bar(x, avg_costs, width, color="orange")
plt.xticks(x, ["Greedy (Influence)", "Greedy (Cost)", "Greedy (Influence/Cost)"])
plt.xlabel("Heuristics")
plt.ylabel("Avg Cost")
plt.title("Average Costs of Greedys")
axes = plt.gca()
axes.set_ylim([0, brute_avg_cost])

# influence distribution
influences = open("influences.txt", "r").readlines()
influences = [float(_) for _ in influences]
plt.figure()
plt.hist(influences)
plt.ylabel("Influence")
plt.title("Distribution of Influence Values From Influence Table")

raw_influences = open("raw_influences.txt", "r").readlines()
raw_influences = [float(_) for _ in raw_influences]
plt.figure()
plt.hist(raw_influences)
plt.ylabel("Influence")
plt.title("Distribution of Raw Influence Values (0-1)")

plt.show()
