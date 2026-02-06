import math
import random
import string
import pandas as pd
import csv

BILLBOARD_CNT = 10
LOCATION_NAME_LEN = 5
MIN_COST = 10
MAX_COST = 100

MIN_POPULATION_CNT = 100
MAX_POPULATION_CNT = 100
MIN_SLOTS_VISITED = 10
MAX_SLOTS_VISITED = 30

MIN_SLOT_CNT = 20
MAX_SLOT_CNT = 20
MAX_INITIAL_SLOT_TIME = 0
MAX_SLOT_DURATION = 10

MIN_TAG_CNT = 8
MAX_TAG_CNT = 8

BUDGET = 1000


def data(
    billboard_count=BILLBOARD_CNT,
    location_name_len=LOCATION_NAME_LEN,
    min_cost=MIN_COST,
    max_cost=MAX_COST,
    min_population_count=MIN_POPULATION_CNT,
    max_population_count=MAX_POPULATION_CNT,
    min_slots_visisted=MIN_SLOTS_VISITED,
    max_slots_visited=MAX_SLOTS_VISITED,
    min_slot_count=MIN_SLOT_CNT,
    max_slot_count=MAX_SLOT_CNT,
    max_initial_slot_time=MAX_INITIAL_SLOT_TIME,
    max_slot_duration=MAX_SLOT_DURATION,
    min_tag_count=MIN_TAG_CNT,
    max_tag_count=MAX_TAG_CNT,
    budget=BUDGET,
):
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
    pd.DataFrame(billboards, columns=["location", "cost"]).rename_axis(
        index="id"
    ).to_csv("billboards.csv")

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

    # population database
    population_cnt = random.randint(MIN_POPULATION_CNT, MAX_POPULATION_CNT)
    population = []
    for i in range(population_cnt):
        rnd_slots = random.choices(
            slots, k=random.choice([MIN_SLOTS_VISITED, MAX_SLOTS_VISITED])
        )
        for slot in rnd_slots:
            location = billboards[slot[0]][0]
            timestamp_start = slot[1]
            timestamp_stop = slot[2]
            population.append([location, timestamp_start, timestamp_stop])
    pd.DataFrame(population, columns=["location", "start", "stop"]).rename_axis(
        index="id"
    ).to_csv("population.csv")

    # influence table
    # 0 if slot timestamp does not agree with user timestamp
    tag_cnt = random.randint(MIN_TAG_CNT, MAX_TAG_CNT)
    influences_table = []
    influences_file = open("influences.txt", "w")
    raw_influences_file = open("raw_influences.txt", "w")
    for tag in range(tag_cnt):
        for slot in range(len(slots)):
            total_influence = 0
            for user in range(len(population)):
                if (
                    max(population[user][1], slots[slot][1])
                    < min(population[user][2], slots[slot][2])
                    and population[user][0] == billboards[slots[slot][0]][0]
                ):
                    influence = random.random()
                    raw_influences_file.write(f"{influence}\n")
                    total_influence += influence
            cost = billboards[slots[slot][0]][1]
            influences_table.append([total_influence, tag, slot, cost])
            influences_file.write(f"{total_influence}\n")
    pd.DataFrame(
        influences_table, columns=["influence", "tag", "slot", "cost"]
    ).rename_axis(index="id").to_csv("influence_table.csv")

    # meta information
    with open("meta.csv", "w") as metafile:
        metawriter = csv.writer(metafile)
        metawriter.writerow(["tag count", "budget"])
        metawriter.writerow([tag_cnt, BUDGET])
