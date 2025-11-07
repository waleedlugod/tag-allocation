import pandas as pd

billboards = pd.read_csv("billboards.csv").to_numpy()
slots = pd.read_csv("slots.csv").to_numpy()
influence_table = pd.read_csv("influence_table.csv").to_numpy()
meta = pd.read_csv("meta.csv").to_numpy()

BUDGET = meta[0][1]

tag_count = meta[0][0]

memo = [
    [
        {"profit": 0, "prev_coords": [-1, -1], "allocated_tag": -1}
        for _ in range(BUDGET + 1)
    ]
    for _ in range(len(slots) + 1)
]

max_influence_of_slots = [[-1, -1]] * len(slots)  # [influence, tag]
for i in influence_table:
    tag_slot_influence = max_influence_of_slots[int(i[3])][0]
    if i[1] > tag_slot_influence:
        max_influence_of_slots[int(i[3])] = [float(i[1]), int(i[2])]

for s in range(len(slots) + 1):
    for w in range(BUDGET + 1):
        slot_weight = billboards[slots[s - 1][1]][2] if s > 0 else 0

        # if sub-weight is 0 or no slots are considered
        if w == 0 or s == 0:
            memo[s][w]["profit"] = 0
        # if weight of the slot considered is within sub-weight
        elif slot_weight <= w:
            # get max influence from influences of a slot
            profit = max_influence_of_slots[s - 1]

            memo[s][w]["profit"] = float(
                max(
                    memo[s - 1][w]["profit"],
                    memo[s - 1][w - slot_weight]["profit"] + profit[0],
                )
            )
            # update allocations
            if memo[s][w]["profit"] > memo[s - 1][w]["profit"]:
                memo[s][w]["prev_coords"] = [s - 1, w - slot_weight]
                memo[s][w]["allocated_tag"] = profit[1]
            else:
                memo[s][w]["prev_coords"] = [s - 1, w]

        # copy values of previous row
        else:
            memo[s][w]["profit"] = memo[s - 1][w]["profit"]
            # update allocations
            memo[s][w]["prev_coords"] = [s - 1, w]


# find allocations
Q = [-1 for _ in range(len(slots))]
coords = [len(slots), BUDGET]
idx = len(slots) - 1
while idx > -1:
    Q[idx] = memo[coords[0]][coords[1]]["allocated_tag"]
    coords = memo[coords[0]][coords[1]]["prev_coords"]
    idx -= 1

total_cost = 0
for slot in range(len(Q)):
    if Q[slot] != -1:
        total_cost += billboards[slots[slot][1]][2]
total_influence = memo[-1][-1]["profit"]

print(
    Q,
    {
        "total influence": format(memo[-1][-1]["profit"], ".4f"),
        "total cost": total_cost,
        "BUDGET": format(BUDGET, ".0f"),
    },
)
