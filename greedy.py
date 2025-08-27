import random
import pandas as pd

MAX_COST = 3

billboards_df = pd.read_csv("billboards.csv")
population_df = pd.read_csv("population.csv")
slots_df = pd.read_csv("slots.csv")
influence_table_df = pd.read_csv("influence_table.csv").sort_values(
    "influence", ascending=False
)
tags_df = pd.read_csv("tags.csv")

Q = [-1 for _ in range(len(slots_df))]
allocated_slots_cnt = 0

tags_cnt = (tags_df.to_numpy())[0][0]
tags = [0 for i in range(tags_cnt)]
allocated_tags = set()


# allocate as much slots as possible to a tag
# tags are not allocated if influence of slot is 0
total_cost = 0
total_influence = 0
billboards = billboards_df.to_numpy()
slots = slots_df.to_numpy()
influence_table = influence_table_df.to_numpy()
# if each tags needs to be allocated to a slot first
# i = 0
# while (
#     allocated_slots_cnt < len(Q) and i < len(influence_table) and total_cost < MAX_COST
# ):
#     influence = influence_table[i]
#     slot = int(influence[3])
#     billboard = int(slots[slot][1])
#     cost = int(billboards[billboard][2])
#     tag = int(influence[2])
#     if (
#         Q[slot] == -1  # slot is free
#         and influence[1] > 0  # influence of slot is greater than 0
#         and total_cost + cost <= MAX_COST
#         and tag not in allocated_tags
#     ):
#         Q[slot] = tag
#         allocated_slots_cnt += 1
#         allocated_tags.add(tag)
#         total_cost += cost
#         total_influence += influence[1]
#     i += 1

i = 0
while (
    allocated_slots_cnt < len(Q) and i < len(influence_table) and total_cost < MAX_COST
):
    influence = influence_table[i]
    slot = int(influence[3])
    billboard = int(slots[slot][1])
    cost = int(billboards[billboard][2])
    tag = int(influence[2])
    if (
        Q[slot] == -1  # slot is free
        and influence[1] > 0  # influence of slot is greater than 0
        and total_cost + cost <= MAX_COST
    ):
        Q[slot] = tag
        allocated_slots_cnt += 1
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
