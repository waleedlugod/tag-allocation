import random
import string
import pandas as pd

LOCATION_CNT = 10

BILLBOARD_CNT = 10
LOCATION_LEN = 5
MAX_COST = 50

POPULATION_CNT = 10
MAX_TIMESTAMP = 200

MAX_SLOT_CNT = 20
MAX_INITIAL_SLOT_TIME = 10
MAX_SLOT_DURATION = 30


locations = []
for i in range(LOCATION_CNT):
    locations.append(
        "".join(random.choices(string.ascii_uppercase + string.digits, k=LOCATION_LEN))
    )

# population database
population = []
for i in range(POPULATION_CNT):
    location = random.choice(locations)
    timestamp_start = random.randint(0, MAX_TIMESTAMP - 1)
    timestamp_stop = random.randint(timestamp_start, MAX_TIMESTAMP)
    population.append([location, timestamp_start, timestamp_stop])
pd.DataFrame(
    population, columns=["location", "timestamp_start", "timestamp_stop"]
).rename_axis(index="id").to_csv("population.csv")

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

# tag database

# influence table
# tag x slot x user = influence
# 0 if slot timestamp does not agree with user timestamp
tag_cnt = 20
influences = []
for tag in range(tag_cnt):
    for slot in range(len(slots)):
        for user in range(len(population)):
            influence = random.random()
            influences.append([format(influence, ".4f"), tag, slot, user])
pd.DataFrame(influences, columns=["influence", "tag", "slot", "user"]).rename_axis(
    index="id"
).to_csv("influence.csv")
