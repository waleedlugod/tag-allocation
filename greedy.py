import pandas as pd

billboards_df = pd.read_csv("billboards.csv")
population_df = pd.read_csv("population.csv")
slots_df = pd.read_csv("slots.csv")
influence_table_df = pd.read_csv("influence_table.csv").sort_values(
    "influence", ascending=False
)
tags_df = pd.read_csv("tags.csv")

tags_cnt = (tags_df.to_numpy())[0][0]
tags = [0 for i in range(tags_cnt)]
print(tags)

# for influence in influence_table_df.to_numpy():
#     print(influence)
