import random
import string
import pandas as pd
import csv

MAX_LOCATION_CNT = 5

BILLBOARD_CNT = 2
LOCATION_LEN = 5
MAX_COST = 20

MAX_POPULATION_CNT = 2
MAX_TIMESTAMP = 20

MAX_SLOT_CNT = 2
MAX_INITIAL_SLOT_TIME = 0
MAX_SLOT_DURATION = 15

MIN_TAG_CNT = 0
MAX_TAG_CNT = 4

BUDGET = 15


location_cnt = random.randint(1, MAX_LOCATION_CNT)
locations = []
for i in range(location_cnt):
    locations.append(
        "".join(random.choices(string.ascii_uppercase + string.digits, k=LOCATION_LEN))
    )

# population database
population_cnt = random.randint(1, MAX_POPULATION_CNT)
population = []
for i in range(population_cnt):
    location = random.choice(locations)
    timestamp_start = random.randint(0, MAX_TIMESTAMP - 1)
    timestamp_stop = random.randint(timestamp_start, MAX_TIMESTAMP)
    population.append([location, timestamp_start, timestamp_stop])
pd.DataFrame(population, columns=["location", "start", "stop"]).rename_axis(
    index="id"
).to_csv("population.csv")

# billboard database
billboards = []
for i in range(BILLBOARD_CNT):
    location = random.choice(locations)
    cost = random.randint(1, MAX_COST)
    billboards.append([location, cost])
pd.DataFrame(billboards, columns=["location", "cost"]).rename_axis(index="id").to_csv(
    "billboards.csv"
)

# slots database
slots = []
for billboard in range(BILLBOARD_CNT):
    slot_cnt = random.randint(1, MAX_SLOT_CNT)
    initial = random.randint(0, MAX_INITIAL_SLOT_TIME)
    duration = random.randint(1, MAX_SLOT_DURATION)
    for slot in range(slot_cnt):
        slots.append([billboard, initial, initial + duration])
        initial += duration + 1
pd.DataFrame(slots, columns=["billboard", "start", "stop"]).rename_axis(
    index="id"
).to_csv("slots.csv")

# influence table
# 0 if slot timestamp does not agree with user timestamp
tag_cnt = random.randint(MIN_TAG_CNT, MAX_TAG_CNT)
influences_table = []
for tag in range(tag_cnt):
    for slot in range(len(slots)):
        total_influence = 0
        for user in range(len(population)):
            if max(population[user][1], slots[slot][1]) < min(
                population[user][2], slots[slot][2]
            ):
                influence = random.random()
                total_influence += influence
        influences_table.append([format(total_influence, ".4f"), tag, slot])
pd.DataFrame(influences_table, columns=["influence", "tag", "slot"]).rename_axis(
    index="id"
).to_csv("influence_table.csv")

# meta information
with open("meta.csv", "w") as metafile:
    metawriter = csv.writer(metafile)
    metawriter.writerow(["tag count", "budget"])
    metawriter.writerow([tag_cnt, BUDGET])
