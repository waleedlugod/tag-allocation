import random
import string
import pandas as pd

LOCATION_CNT = 10

DATABASE_CNT = 10
LOCATION_LEN = 5
MAX_COST = 50

POPULATION_CNT = 10
MAX_TIMESTAMP = 100


locations = []
for i in range(LOCATION_CNT):
    locations.append(
        "".join(random.choices(string.ascii_uppercase + string.digits, k=LOCATION_LEN))
    )


# billboard database
billboards = []
for i in range(DATABASE_CNT):
    location = random.choice(locations)
    cost = random.randint(1, MAX_COST)
    billboards.append([location, cost])
pd.DataFrame(billboards, columns=["location", "cost"]).rename_axis(index="id").to_csv(
    "billboards.csv"
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
