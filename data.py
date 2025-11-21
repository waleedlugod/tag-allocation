import math
import random
import string
import pandas as pd
import csv

BILLBOARD_CNT = 2
LOCATION_NAME_LEN = 5
MIN_COST = 5
MAX_COST = 10

MIN_POPULATION_CNT = 20
MAX_POPULATION_CNT = 60
MAX_TIMESTAMP = 15

MIN_SLOT_CNT = 2
MAX_SLOT_CNT = 2
MAX_INITIAL_SLOT_TIME = 0
MAX_SLOT_DURATION = 3

MIN_TAG_CNT = 2
MAX_TAG_CNT = 3

BUDGET = 15


# billboard database
locations = []
billboards = []
for i in range(BILLBOARD_CNT):
    location = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=LOCATION_NAME_LEN)
    )
    locations.append(location)
    cost = random.randint(MIN_COST, MAX_COST)
    billboards.append([location, cost])
pd.DataFrame(billboards, columns=["location", "cost"]).rename_axis(index="id").to_csv(
    "billboards.csv"
)

# population database
population_cnt = random.randint(MIN_POPULATION_CNT, MAX_POPULATION_CNT)
population = []
for i in range(population_cnt):
    location = random.choice(locations)
    timestamp_start = random.randint(0, MAX_TIMESTAMP - 1)
    timestamp_stop = random.randint(timestamp_start, MAX_TIMESTAMP)
    population.append([location, timestamp_start, timestamp_stop])
pd.DataFrame(population, columns=["location", "start", "stop"]).rename_axis(
    index="id"
).to_csv("population.csv")

# slots database
slots = []
for billboard in range(BILLBOARD_CNT):
    initial = random.randint(0, MAX_INITIAL_SLOT_TIME)
    duration = random.randint(1, MAX_SLOT_DURATION)
    slot_cnt = random.randint(MIN_SLOT_CNT, MAX_SLOT_CNT)
    for slot in range(math.floor(slot_cnt)):
        slots.append([billboard, initial, initial + duration])
        initial += duration + 1
pd.DataFrame(slots, columns=["billboard", "start", "stop"]).rename_axis(
    index="id"
).to_csv("slots.csv")

# influence table
# 0 if slot timestamp does not agree with user timestamp
tag_cnt = random.randint(MIN_TAG_CNT, MAX_TAG_CNT)
influences_table = []
influences_file = open("influences.txt", "a")
for tag in range(tag_cnt):
    for slot in range(len(slots)):
        total_influence = 0
        for user in range(len(population)):
            if max(population[user][1], slots[slot][1]) < min(
                population[user][2], slots[slot][2]
            ) and population[user][0]==billboards[slots[slot][0]][0]:
                influence = random.random()
                total_influence += influence
        cost = billboards[slots[slot][0]][1]
        influences_table.append([format(total_influence, ".4f"), tag, slot, cost])
        influences_file.write(f"{total_influence}\n")
pd.DataFrame(
    influences_table, columns=["influence", "tag", "slot", "cost"]
).rename_axis(index="id").to_csv("influence_table.csv")

# meta information
with open("meta.csv", "w") as metafile:
    metawriter = csv.writer(metafile)
    metawriter.writerow(["tag count", "budget"])
    metawriter.writerow([tag_cnt, BUDGET])
