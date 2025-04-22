import random
import string
import pandas as pd

N=5
max_cost = 50

b_locs = []
b_costs = []
for i in range(10):
    b_locs.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=N)))
    b_costs.append(random.randint(1, max_cost))

billboards ={'locations': b_locs, 'cost': b_costs}
pd.DataFrame(billboards).to_csv("billboards.csv")
