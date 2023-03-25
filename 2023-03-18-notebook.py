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

# Prepare food df
food_logs_loc = (root_dir / "CarbManager/daily_logs_20210312-20230318_fe628b90-9859-4259-ab49-1ba3ce95b90c.csv")
food_df = pd.read_csv(food_logs_loc)

cols = ["RawDate", "Meal", "Calories"]
food_df["RawDate"] = food_df["Date"].map(lambda x: x.split(" ")[0])
food_df[food_df.Meal.isin(["Snack", "Dinner", "Lunch", "Breakfast"])][cols].iloc[-10:]
food_agg_df = food_df[["RawDate", "Calories"]].groupby(by=["RawDate"]).sum().reset_index()


weight_loc = root_dir / ("withings/2023-03-18-data_MIC_1679186118/weight.csv")
weight_df = pd.read_csv(weight_loc)
cols = ["Date", "Weight (lb)"]
weight_df[cols].sort_values(by="Date").iloc[-10:]
weight_df["RawDate"] = weight_df["Date"].map(lambda x: x.split(" ")[0])
cols = ["RawDate", "Weight (lb)"]
weight_agg_df = weight_df[cols].groupby(by="RawDate").min().reset_index()

start_date = date(2022, 1, 1) # "2023-01-01"
end_date = date(2023, 3, 17)
X = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") 
     for i in range((end_date - start_date).days)]
fig = plt.figure(figsize=(12, 4))
ax1 = fig.add_subplot(111)

data1 =  food_agg_df[food_agg_df["RawDate"] >= start_date.strftime("%Y-%m-%d")
                     ].to_dict(orient="list")
color = "tab:red"
x1, y1 = data1["RawDate"], data1["Calories"]
ax1.plot(x1, y1, color=color)
ax1.set_xlabel("Date")
ax1.set_ylabel("Calories", color=color)
x_ticks, x_labels = make_xtick_labels(X, step=14)
ax1.set_xticks(x_ticks)
ax1.set_xticklabels(x_labels, rotation=-45)

# weight data, 
color = "tab:blue"
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel("Weight (lb)", color=color)
data2 = weight_agg_df[weight_agg_df["RawDate"] >= start_date.strftime("%Y-%m-%d")
                     ].to_dict(orient="list")
x2, y2 = data2["RawDate"], data2["Weight (lb)"]
ax2.plot(x2, y2, color=color)


out_loc = f"output-data/{utc_ts()}-figure.png"
pylab.savefig(out_loc, bbox_inches='tight')
