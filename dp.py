import pandas as pd

billboards = pd.read_csv("billboards.csv").to_numpy()
slots = pd.read_csv("slots.csv").to_numpy()
influence_table = pd.read_csv("influence_table.csv").to_numpy()
meta = pd.read_csv("meta.csv").to_numpy()

Q = [-1 for _ in range(len(slots))]

BUDGET = meta[0][1]

tag_count = meta[0][0]

memo = [[0 for _ in range(BUDGET + 1)] for _ in range(len(slots) + 1)]
memoQ = [
    [[-1 for _ in range(len(slots))] for _ in range(BUDGET + 1)]
    for _ in range(len(slots) + 1)
]

for s in range(len(slots) + 1):
    for w in range(BUDGET + 1):
        slot_weight = billboards[slots[s - 1][1]][2] if s > 0 else 0

        # if sub-weight is 0 or no slots are considered
        if w == 0 or s == 0:
            memo[s][w] = 0
        # if weight of the slot considered is within sub-weight
        elif slot_weight <= w:
            # get max influence from influences of a slot
            first_idx = (s - 1) * tag_count
            last_idx = (s - 1) * tag_count + tag_count
            influences_of_slot = [_ for _ in influence_table[first_idx:last_idx]]
            # find max and index of max
            profit = influences_of_slot[0][1]
            profit_idx = 0
            for i in range(len(influences_of_slot)):
                if influences_of_slot[i][1] > profit:
                    profit = influences_of_slot[i][1]
                    profit_idx = i

            memo[s][w] = float(
                max(memo[s - 1][w], memo[s - 1][w - slot_weight] + profit)
            )

            # update allocations (Q)
            if memo[s][w] > memo[s - 1][w]:
                for _ in range(len(slots)):
                    memoQ[s][w][_] = memoQ[s - 1][w - slot_weight][_]
                memoQ[s][w][s - 1] = profit_idx
            else:
                for _ in range(len(slots)):
                    memoQ[s][w][_] = memoQ[s - 1][w][_]

        # copy values of previous row
        else:
            memo[s][w] = memo[s - 1][w]
            for _ in range(len(slots)):
                memoQ[s][w][_] = memoQ[s - 1][w][_]

Q = memoQ[-1][-1]
final_cost = 0
for slot in range(len(Q)):
    if Q[slot] != -1:
        final_cost += billboards[slots[slot][1]][2]

print(
    Q,
    {
        "total influence": format(memo[-1][-1], ".4f"),
        "total cost": final_cost,
        "BUDGET": format(BUDGET, ".0f"),
    },
)
