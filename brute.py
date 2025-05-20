import random
from itertools import permutations

import pandas as pd

billboards_df = pd.read_csv("billboards.csv")
population_df = pd.read_csv("population.csv")
slots_df = pd.read_csv("slots.csv")
influence_table_df = pd.read_csv("influence_table.csv").sort_values(
    "influence", ascending=False
)
tags_df = pd.read_csv("tags.csv")

billboards = billboards_df.to_numpy()[:4]
slots = slots_df.to_numpy()[:4]
influence_table = influence_table_df.to_numpy()

final_cost = 0
total_cost = 0
for slot in slots:
    billboard = slot[1]
    cost = billboards[billboard][2]
    total_cost += cost

MAX_COST = random.randint(1, total_cost + (total_cost // 3))

MAX_INFLUENCE = -1

Q = [-1 for _ in range(len(slots))]
allocated_slots = 0

tags_cnt = 4
tags = [0 for _ in range(tags_cnt)]

# Try all combinations of tags
for i in range(1 << tags_cnt):
    tags_comb = []
    for j in range(tags_cnt):
        if i & 1 << j:
            tags_comb.append(j)

    # Get all permutations of current tag combination
    tags_perms = list(permutations(tags_comb))

    # Try all combinations of slots
    slots_comb = []
    for k in range(1 << len(slots)):
        slots_comb = []
        for l in range(len(slots)):
            if k & 1 << l:
                slots_comb.append(l)

        # Get all permutations of current slot combination
        slots_perms = list(permutations(slots_comb))

        # For each tag permutation to slot permutation
        # First, check if valid allocation
        # If valid allocation, get influence
        for tag_perm in tags_perms:
            for slot_perm in slots_perms:
                curr_allocation = [-1 for _ in range(len(slots))]
                valid_allocation = True
                slots_taken = []
                curr_influence = 0
                curr_cost = 0

                for l in range(min(len(tag_perm), len(slot_perm))):
                    slot = slot_perm[l]
                    billboard = int(slots[slot][1])

                    if len(slots_taken) > 0:
                        for other_slot in slots_taken:
                            if other_slot[1] != slots[slot][1]:
                                continue

                            if (
                                other_slot[2] <= slots[slot][2]
                                and other_slot[3] > slots[slot][2]
                            ):
                                valid_allocation = False
                                break
                    slots_taken.append(slots[slot])

                    cost = int(billboards[billboard][2])
                    for influence in influence_table:
                        if influence[2] == tag_perm[l] and influence[3] == slot:
                            curr_allocation[slot] = int(influence[2])
                            curr_influence += influence[1]
                            curr_cost += cost
                            break

                # If current matching is best, store it
                if (
                    valid_allocation
                    and curr_cost <= MAX_COST
                    and curr_influence > MAX_INFLUENCE
                ):
                    Q = curr_allocation
                    MAX_INFLUENCE = curr_influence
                    final_cost = curr_cost

print(
    Q,
    {
        "total influence": format(MAX_INFLUENCE, ".4f"),
        "total cost": final_cost,
        "MAX COST": MAX_COST,
    },
)
