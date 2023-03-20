import os
import matplotlib.pyplot as plt
import pandas as pd
import pylab
from pathlib import Path
from datetime import datetime, date, timedelta

from core.date_utils import utc_ts


def make_xtick_labels(x, step=5):
    '''Given x, step the labels every <step>
    Aka, take every <step>th x label
    '''
    x_ticks = [i for i in  range(len(x)) if i % step == 0]
    x_labels = [x[i] for i in x_ticks]
    return x_ticks, x_labels

root_dir = Path(os.getenv("ROOT_DIR"))
food_logs_loc = (root_dir / "CarbManager/daily_logs_20210312-20230318_fe628b90-9859-4259-ab49-1ba3ce95b90c.csv")
weight_loc = root_dir / ("withings/2023-03-18-data_MIC_1679186118/weight.csv")
food_df = pd.read_csv(food_logs_loc)
weight_df = pd.read_csv(weight_loc)

cols = ["RawDate", "Meal", "Calories"]
food_df["RawDate"] = food_df["Date"].map(lambda x: x.split(" ")[0])
food_df[food_df.Meal.isin(["Snack", "Dinner", "Lunch", "Breakfast"])][cols].iloc[-10:]

In [30]: food_df[["RawDate", "Calories"]].groupby(by=["RawDate"]).sum().Calories.describe()
Out[30]: 
count     452.000000
mean     2673.786062
std       778.165650
min         0.000000
25%      2296.875000
50%      2685.450000
75%      3098.575000
max      5062.000000
Name: Calories, dtype: float64
    
    
food_agg_df = food_df[["RawDate", "Calories"]].groupby(by=["RawDate"]).sum().reset_index()


cols = ["RawDate", "Weight (lb)"]
weight_df[cols].sort_values(by="Date").iloc[-10:]
weight_df["RawDate"] = weight_df["Date"].map(lambda x: x.split(" ")[0])

start_date = date(2023, 1, 1) # "2023-01-01"
end_date = date(2023, 3, 17)
x = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") 
     for i in range((end_date - start_date).days)]
fig = plt.figure(figsize=(12, 4))
ax = fig.add_subplot(111)

data =  food_agg_df[food_agg_df["RawDate"] >= start_date.strftime("%Y-%m-%d")
                     ].to_dict(orient="list")
x1, y1 = data["RawDate"], data["Calories"]
ax.plot(x1, y1)
x_ticks, x_labels = make_xtick_labels(x, step=7)
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=-45)
# fig.show()


out_loc = "/Users/michal/Dropbox/Code/repo/fasting-analyze/output-data/blah.png"
pylab.savefig(out_loc, bbox_inches='tight')
