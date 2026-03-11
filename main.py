import importlib
import math
import pandas as pd

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

# heuristics to test
# first heuristic is set as control
heuristics = [
    # "brute",
    "dp",
    "greedy",
    "greedy_cost",
    "greedy_influence_cost_ratio",
    "greedy_influence_cost_slot_ratio",
    "genetic",
]
titles = [
    # "Brute-force",
    "DP",
    "Greedy (Influence)",
    "Greedy (Cost)",
    "Greedy (Influence/Cost)",
    "Greedy (Influence/Cost * Slots)",
    "Genetic (100 population, 250 generations, Default Config)",
]

influences_all = open("influences_all.txt", "w")
raw_influences_all = open("raw_influences_all.txt", "w")
comp_time = ""

results = {}
best_greedy_results = {
    "correct_cnt": 0,
    "agg_approx_ratio": 0,
    "agg_approx_cost": 0,
}
for i in range(len(heuristics)):
    results[heuristics[i]] = {}
    results[heuristics[i]]["title"] = titles[i]
    if i != 0:
        results[heuristics[i]]["correct_cnt"] = 0
        results[heuristics[i]]["agg_approx_ratio"] = 0
        results[heuristics[i]]["agg_approx_cost"] = 0

h = [None] * len(heuristics)


def compute(slot_count=slots_start, budget=budget_start):
    global comp_time
    comp_time += f"Slots: {str(slot_count)}, Budget: {budget}\n"
    for test in range(NUM_TEST_CASES):
        data = importlib.import_module("data")
        influences_all.write(open("influences.txt").read())
        raw_influences_all.write(open("raw_influences.txt").read())
        data.data(slot_count=slot_count, budget=budget)

        for i in range(len(heuristics)):
            print(titles[i])
            h[i] = importlib.import_module(heuristics[i])
            importlib.reload(h[i])
            comp_time += f"computation time: {str(h[i].end_time - h[i].start_time)} seconds {titles[i]}\n"

    max_greedy_cost = -1
    max_greedy_approx_ratio = -1
    max_influence = -1
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
        
        if heuristics[i] == "genetic":
            continue
        
        curr_approx_cost = h[i].total_cost / h[0].total_cost if not math.isclose(0, h[0].total_cost, rel_tol=1e-6) else 1
        curr_approx_ratio = h[i].total_influence / h[0].total_influence if not math.isclose(0, h[0].total_influence, rel_tol=1e-6) else 1
        if max(max_greedy_approx_ratio, curr_approx_ratio) == curr_approx_ratio:
            max_greedy_approx_ratio = curr_approx_ratio
            max_greedy_cost = curr_approx_cost
            max_influence = h[i].total_influence

    best_greedy_results["agg_approx_cost"] += max_greedy_cost
    best_greedy_results["agg_approx_ratio"] += max_greedy_approx_ratio
    if math.isclose(h[0].total_influence, max_influence, rel_tol=1e-6):
        best_greedy_results["correct_cnt"] += 1


for b in range(budget_steps):
    budget = budget_start + budget_step * b
    compute(budget=budget)
for s in range(1, slots_steps):
    slot_count = slots_start + slots_step * s
    compute(slot_count=slot_count)

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

best_greedy_results["avg_approx_cost"] = (
    best_greedy_results["agg_approx_cost"] / NUM_TEST_CASES
)
best_greedy_results["avg_approx_ratio"] = (
    best_greedy_results["agg_approx_ratio"] / NUM_TEST_CASES
)
best_greedy_results["performance"] = (
    best_greedy_results["correct_cnt"] / NUM_TEST_CASES
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
    
    f.write(
        f"Best Greedy Performance: {best_greedy_results["performance"]:.2f}\n"
    )
    f.write(
        f"Best Greedy Average Approximation Ratio: {best_greedy_results["avg_approx_ratio"]:.2f}\n"
    )
    f.write(
        f"Best Greedy Average Cost Approximation Ratio: {best_greedy_results["avg_approx_cost"]:.2f}\n"
    )
    f.write(comp_time)
