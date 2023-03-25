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

def get_data():
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
    return food_agg_df, weight_agg_df

def plot_data(food_agg_df, weight_agg_df, start_date, end_date):

    X = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") 
         for i in range((end_date - start_date).days)]

    fig = plt.figure(figsize=(12, 4))
    ax1 = fig.add_subplot(111)

    color = "tab:blue"
    ax1.set_ylabel("Weight (lb)", color=color)
    data1 = weight_agg_df[
        weight_agg_df["RawDate"] >= start_date.strftime("%Y-%m-%d")
    ].to_dict(orient="list")
    x1, y1 = data1["RawDate"], data1["Weight (lb)"]
    x_ticks, x_labels = make_xtick_labels(X, step=14)
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_labels, rotation=-45)

    ax1.plot(x1, y1, color=color)

    # Flip,
    ax2 = ax1.twinx()

    data2 = food_agg_df[food_agg_df["RawDate"] >= start_date.strftime("%Y-%m-%d")].to_dict(
        orient="list"
    )
    color = "tab:red"
    x2, y2 = data2["RawDate"], data2["Calories"]
    ax2.plot(x2, y2, color=color)
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Calories", color=color)
    out_loc = f"output-data/{utc_ts()}-figure.png"
    print("out_loc", out_loc)
    pylab.savefig(out_loc, bbox_inches="tight")

# Plot day by day data,
food_agg_df, weight_agg_df = get_data()
start_date = date(2022, 1, 1) # "2023-01-01"
end_date = date(2023, 3, 17)

plot_data(start_date, end_date)

# Try 3 day average of weight, and 3 day total, for calories, 

weight_agg_df["timestamp"] = pd.to_datetime(weight_agg_df["RawDate"])
weight_agg_3day_df = weight_agg_df.groupby(pd.Grouper(key='timestamp', freq='3D')).mean().reset_index()
weight_agg_3day_df["RawDate"] = weight_agg_3day_df["timestamp"].map(lambda x:x.strftime("%Y-%m-%d"))

food_agg_df["timestamp"] =  pd.to_datetime(food_agg_df["RawDate"])
food_agg_3day_df = food_agg_df.groupby(pd.Grouper(key='timestamp', freq='3D')).mean().reset_index()
food_agg_3day_df["RawDate"] = food_agg_3day_df["timestamp"].map(lambda x:x.strftime("%Y-%m-%d"))

plot_data(food_agg_3day_df, weight_agg_3day_df, start_date, end_date)
