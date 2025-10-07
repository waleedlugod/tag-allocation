import importlib
import math

NUM_TEST_CASES = 100

num_correct = {
    "brute": {"avg_cost": 0},
    "greedy": {"correct_cnt": 0, "avg_cost": 0, "avg_approx_ratio": 0},
    "greedy_cost": {"correct_cnt": 0, "avg_cost": 0, "avg_approx_ratio": 0},
    "greedy_influence_cost_ratio": {
        "correct_cnt": 0,
        "avg_cost": 0,
        "avg_approx_ratio": 0,
    },
}

influences_file = open("influences.txt", "w")

for test_case in range(1, NUM_TEST_CASES + 1):
    data = importlib.import_module("data")
    importlib.reload(data)

    brute = importlib.import_module("brute")
    importlib.reload(brute)

    greedy = importlib.import_module("greedy")
    importlib.reload(greedy)

    greedy_cost = importlib.import_module("greedy_cost")
    importlib.reload(greedy_cost)

    greedy_influence_cost_ratio = importlib.import_module("greedy_influence_cost_ratio")
    importlib.reload(greedy_influence_cost_ratio)

    num_correct["brute"]["avg_cost"] += brute.final_cost

    num_correct["greedy"]["avg_cost"] += greedy.total_cost
    num_correct["greedy_cost"]["avg_cost"] += greedy_cost.total_cost
    num_correct["greedy_influence_cost_ratio"][
        "avg_cost"
    ] += greedy_influence_cost_ratio.total_cost

    num_correct["greedy"]["avg_approx_ratio"] += (
        greedy.total_influence / brute.MAX_INFLUENCE
        if not math.isclose(0, brute.MAX_INFLUENCE, rel_tol=1e-6)
        else 1
    )
    num_correct["greedy_cost"]["avg_approx_ratio"] += (
        greedy_cost.total_influence / brute.MAX_INFLUENCE
        if not math.isclose(0, brute.MAX_INFLUENCE, rel_tol=1e-6)
        else 1
    )
    num_correct["greedy_influence_cost_ratio"]["avg_approx_ratio"] += (
        greedy_influence_cost_ratio.total_influence / brute.MAX_INFLUENCE
        if not math.isclose(0, brute.MAX_INFLUENCE, rel_tol=1e-6)
        else 1
    )

    if math.isclose(brute.MAX_INFLUENCE, greedy.total_influence, rel_tol=1e-6):
        num_correct["greedy"]["correct_cnt"] += 1
    if math.isclose(brute.MAX_INFLUENCE, greedy_cost.total_influence, rel_tol=1e-6):
        num_correct["greedy_cost"]["correct_cnt"] += 1
    if math.isclose(
        brute.MAX_INFLUENCE, greedy_influence_cost_ratio.total_influence, rel_tol=1e-6
    ):
        num_correct["greedy_influence_cost_ratio"]["correct_cnt"] += 1

num_correct["brute"]["avg_cost"] /= NUM_TEST_CASES
num_correct["greedy"]["avg_cost"] /= NUM_TEST_CASES
num_correct["greedy_cost"]["avg_cost"] /= NUM_TEST_CASES
num_correct["greedy_influence_cost_ratio"]["avg_cost"] /= NUM_TEST_CASES

num_correct["greedy"]["avg_approx_ratio"] /= NUM_TEST_CASES
num_correct["greedy_cost"]["avg_approx_ratio"] /= NUM_TEST_CASES
num_correct["greedy_influence_cost_ratio"]["avg_approx_ratio"] /= NUM_TEST_CASES

with open("output.txt", "w") as outputf:
    outputf.writelines(
        [
            f"Brute-force Average Cost: {num_correct['brute']['avg_cost']}\n",
            f"Greedy (Influence) Performance: {num_correct['greedy']['correct_cnt']/NUM_TEST_CASES}\n",
            f"Greedy (Influence) Average Approximation Ratio: {num_correct['greedy']['avg_approx_ratio']}\n",
            f"Greedy (Influence) Average Cost: {num_correct['greedy']['avg_cost']}\n",
            f"Greedy (Cost) Performance: {num_correct['greedy_cost']['correct_cnt']/NUM_TEST_CASES}\n",
            f"Greedy (Cost) Average Approximation Ratio: {num_correct['greedy_cost']['avg_approx_ratio']}\n",
            f"Greedy (Cost) Average Cost: {num_correct['greedy_cost']['avg_cost']}\n",
            f"Greedy (Influence/Cost) Performance: {num_correct['greedy_influence_cost_ratio']['correct_cnt']/NUM_TEST_CASES}\n",
            f"Greedy (Influence/Cost) Average Approximation Ratio: {num_correct['greedy_influence_cost_ratio']['avg_approx_ratio']}\n",
            f"Greedy (Influence/Cost) Average Cost: {num_correct['greedy_influence_cost_ratio']['avg_cost']}",
        ]
    )
