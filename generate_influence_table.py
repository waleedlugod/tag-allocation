import pandas as pd
import random

meta_df = pd.read_csv("meta.csv")
slots_df = pd.read_csv("slots.csv")
population_df = pd.read_csv("population.csv")
billboards_df = pd.read_csv("billboards.csv")

tags_cnt = (meta_df.to_numpy())[0][0]
slots = slots_df.to_numpy()
population = population_df.to_numpy()
billboards = billboards_df.to_numpy()

margin = 0

influences_table = []
for tag in range(tags_cnt):
    for slot in range(len(slots)):
        total_influence = 0
        for user in range(len(population)):
            if max(population[user][2], slots[slot][2]) < min(
                population[user][3], slots[slot][3]
            ) and population[user][1]==billboards[slots[slot][1]][1]:
                influence = random.random()*(margin*2)+(1-margin)
                total_influence += influence
        cost = billboards[slots[slot][1]][2]
        influences_table.append([format(total_influence, ".4f"), tag, slot, cost])
pd.DataFrame(
    influences_table, columns=["influence", "tag", "slot", "cost"]
).rename_axis(index="id").to_csv("influence_table.csv")

#  and population[user][0]==billboards[slots[slot][0]][0]