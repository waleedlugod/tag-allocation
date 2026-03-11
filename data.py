import math
import random
import string
import pandas as pd
import csv


def data(
    billboard_count=10,
    location_name_len=5,
    min_cost=10000,
    max_cost=100000,
    min_population_count=100,
    max_population_count=100,
    min_slots_visited=10,
    max_slots_visited=30,
    slot_count=20,
    max_initial_slot_time=0,
    max_slot_duration=10,
    min_tag_count=20,
    max_tag_count=20,
    budget=1000,
):
    if min_cost > budget:
        min_cost = budget * 0.10
    if max_cost > budget:
        max_cost = budget * 0.5

    max_slots_visited = budget

    # billboard database
    locations = []
    billboards = []
    for i in range(billboard_count):
        location = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=location_name_len)
        )
        locations.append(location)
        cost = random.randint(min_cost, max_cost)
        billboards.append([location, cost])
    pd.DataFrame(billboards, columns=["location", "cost"]).rename_axis(
        index="id"
    ).to_csv("billboards.csv")

    # slots database
    slots = []
    for billboard in range(billboard_count):
        initial = random.randint(0, max_initial_slot_time)
        duration = random.randint(1, max_slot_duration)
        for slot in range(math.floor(slot_count)):
            slots.append([billboard, initial, initial + duration])
            initial += duration + 1
    pd.DataFrame(slots, columns=["billboard", "start", "stop"]).rename_axis(
        index="id"
    ).to_csv("slots.csv")

    # population database
    population_cnt = random.randint(min_population_count, max_population_count)
    population = []
    for i in range(population_cnt):
        rnd_slots = random.choices(
            slots, k=random.choice([min_slots_visited, max_slots_visited])
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
    tag_cnt = random.randint(min_tag_count, max_tag_count)
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
        metawriter.writerow([tag_cnt, budget])
