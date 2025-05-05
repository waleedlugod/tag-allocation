import random
import pandas as pd

MAX_COST = random.randint(1, 500)

billboards_df = pd.read_csv("billboards.csv")
population_df = pd.read_csv("population.csv")
slots_df = pd.read_csv("slots.csv")
influence_table_df = pd.read_csv("influence_table.csv").sort_values(
    "influence", ascending=False
)
tags_df = pd.read_csv("tags.csv")

Q = [-1 for _ in range(len(slots_df))]
allocated_slots = 0

tags_cnt = (tags_df.to_numpy())[0][0]
tags = [0 for i in range(tags_cnt)]

total_cost = 0
total_influence = 0
tags_added = set()
billboards = billboards_df.to_numpy()
slots = slots_df.to_numpy()
influence_table = influence_table_df.to_numpy()
for influence in influence_table:
    slot = int(influence[3])
    billboard = int(slots[slot][1])
    cost = int(billboards[billboard][2])
    if int(influence[2]) not in tags_added and Q[int(influence[3])] == -1:
        tags_added.add(int(influence[2]))
        Q[int(influence[3])] = int(influence[2])
        allocated_slots += 1
        total_cost += cost
        total_influence += influence[1]

i = 0
while allocated_slots < len(Q) and i < len(influence_table) and total_cost < MAX_COST:
    influence = influence_table[i]
    slot = int(influence[3])
    billboard = int(slots[slot][1])
    cost = int(billboards[billboard][2])
    if Q[int(influence[3])] == -1:
        Q[int(influence[3])] = int(influence[2])
        allocated_slots += 1
        total_cost += cost
        total_influence += influence[1]
    i += 1

print(
    Q,
    {
        "total influence": format(total_influence, ".4f"),
        "total cost": total_cost,
        "MAX COST": MAX_COST,
    },
)
