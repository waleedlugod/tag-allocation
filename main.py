import importlib
import math
import pandas as pd

settings = pd.read_csv("settings.csv").to_numpy()[0]
NUM_TEST_CASES = settings[0]
start = settings[1]
step = settings[2]
steps = settings[3]

# heuristics to test
# first heuristic is set as control
heuristics = [
    # "brute",
    "dp",
    "greedy",
    "greedy_cost",
    "greedy_influence_cost_ratio",
    "genetic",
]
titles = [
    # "Brute-force",
    "DP",
    "Greedy (Influence)",
    "Greedy (Cost)",
    "Greedy (Influence/Cost)",
    "Genetic (100 population, 250 generations, Default Config)",
]

influences_all = open("influences_all.txt", "w")
raw_influences_all = open("raw_influences_all.txt", "w")

results = {}
for i in range(len(heuristics)):
    results[heuristics[i]] = {}
    results[heuristics[i]]["title"] = titles[i]
    if i != 0:
        results[heuristics[i]]["correct_cnt"] = 0
        results[heuristics[i]]["agg_approx_ratio"] = 0
        results[heuristics[i]]["agg_approx_cost"] = 0

h = [None] * len(heuristics)
for test in range(NUM_TEST_CASES):
    data = importlib.import_module("data")
    influences_all.write(open("influences.txt").read())
    raw_influences_all.write(open("raw_influences.txt").read())
    data.data()

    for i in range(len(heuristics)):
        h[i] = importlib.import_module(heuristics[i])
        importlib.reload(h[i])
        print(
            "computation time: " + str(h[i].end_time - h[i].start_time) + " seconds",
            titles[i],
        )

    for i in range(1, len(heuristics)):
        results[heuristics[i]]["agg_approx_cost"] += (
            h[i].total_cost / h[0].total_cost
            if not math.isclose(0, h[0].total_cost, rel_tol=1e-6)
            else 1
        )
        results[heuristics[i]]["agg_approx_ratio"] += (
            h[i].total_influence / h[0].total_influence
            if not math.isclose(0, h[0].total_influence, rel_tol=1e-6)
            else 1
        )
        if math.isclose(h[0].total_influence, h[i].total_influence, rel_tol=1e-6):
            results[heuristics[i]]["correct_cnt"] += 1


for i in range(1, len(h)):
    results[heuristics[i]]["avg_approx_cost"] = (
        results[heuristics[i]]["agg_approx_cost"] / NUM_TEST_CASES
    )
    results[heuristics[i]]["avg_approx_ratio"] = (
        results[heuristics[i]]["agg_approx_ratio"] / NUM_TEST_CASES
    )
    results[heuristics[i]]["performance"] = (
        results[heuristics[i]]["correct_cnt"] / NUM_TEST_CASES
    )

with open("output.txt", "w") as f:
    for i in range(1, len(heuristics)):
        f.write(
            f"{results[heuristics[i]]['title']} Performance: {results[heuristics[i]]['performance']:.2f}\n"
        )
        f.write(
            f"{results[heuristics[i]]['title']} Average Approximation Ratio: {results[heuristics[i]]['avg_approx_ratio']:.2f}\n"
        )
        f.write(
            f"{results[heuristics[i]]['title']} Average Cost Approximation Ratio: {results[heuristics[i]]['avg_approx_cost']:.2f}\n"
        )
