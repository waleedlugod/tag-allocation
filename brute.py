import random
from copy import copy

import pandas as pd

billboards_df = pd.read_csv("billboards.csv")
population_df = pd.read_csv("population.csv")
slots_df = pd.read_csv("slots.csv")
influence_table_df = pd.read_csv("influence_table.csv").sort_values(
    "influence", ascending=False
)
tags_df = pd.read_csv("tags.csv")

billboards = billboards_df.to_numpy()[:3]
slots = slots_df.to_numpy()[:3]
influence_table = influence_table_df.to_numpy()

final_cost = 0
total_cost = 0
for slot in slots:
    billboard = slot[1]
    cost = billboards[billboard][2]
    total_cost += cost

MAX_COST = random.randint(1, total_cost + (total_cost // 3))

MAX_INFLUENCE = 0

LOCAL_Q = [-1 for _ in range(len(slots))]
Q = [-1 for _ in range(len(slots))]

tags_cnt = 3
tags = [0 for _ in range(tags_cnt)]
iterate_tags = [i for i in range(-1, tags_cnt)]


def brute(idx, cost):
    global Q
    global LOCAL_Q
    global tags
    global iterate_tags
    global slots
    global billboards
    global MAX_COST
    global MAX_INFLUENCE
    global final_cost
    global influence_table

    if idx >= len(Q):
        curr_influence = 0
        curr_cost = 0

        for i in range(len(Q)):
            if LOCAL_Q[i] == -1:
                continue

            for influence in influence_table:
                if int(influence[2]) == LOCAL_Q[i] and int(influence[3]) == i:
                    curr_influence += influence[1]

                    billboard = slots[i][1]
                    billboard_cost = billboards[billboard][2]
                    curr_cost += billboard_cost

                    break

        if curr_influence > MAX_INFLUENCE and curr_cost <= MAX_COST:
            final_cost = copy(curr_cost)
            MAX_INFLUENCE = copy(curr_influence)
            Q = copy(LOCAL_Q)

        return

    for tag in iterate_tags:
        for influence in influence_table:
            if int(influence[3]) == idx:
                slot = int(influence[3])
                billboard = slots[slot][1]
                billboard_cost = billboards[billboard][2]

                LOCAL_Q[idx] = tag
                brute(idx + 1, cost + billboard_cost)
                LOCAL_Q[idx] = -1


brute(0, 0)

print(
    Q,
    {
        "total influence": format(MAX_INFLUENCE, ".4f"),
        "total cost": final_cost,
        "MAX COST": MAX_COST,
    },
)
