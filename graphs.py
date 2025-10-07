import matplotlib.pyplot as plt
import numpy as np

output = open("output.txt", "r")

HEURISTICS_CNT = 4

performances = []
avg_approx_ratios = []
avg_costs = []

brute_avg_cost = output.readline().split(" ")[-1]
for _ in range(HEURISTICS_CNT - 1):
    performances.append(float(output.readline().split(" ")[-1]))
    avg_approx_ratios.append(float(output.readline().split(" ")[-1]))
    avg_costs.append(float(output.readline().split(" ")[-1]))


x = np.arange(HEURISTICS_CNT - 1)
width = 0.25
print(performances)

plt.bar(x - width, performances, width, color="green")
plt.bar(x, avg_approx_ratios, width, color="orange")
plt.xticks(x, ["Greedy (Influence)", "Greedy (Cost)", "Greedy (Influence/Cost)"])
plt.xlabel("Heuristics")
plt.ylabel("Percent")
plt.legend(["Correctness", "Avg Approximation Ratio"])
plt.show()
