import datetime
import yaml
import core.feature_funcs as ff


def build_dataset(df):

    # Base annotations
    df["StartDt"] =  df.apply(lambda x: datetime.datetime(int(f"20{x.Date.split('/')[2]}"),
                                                          int(x.Date.split("/")[0]),
                                                          int(x.Date.split("/")[1]),
                                                          int(x.Start.split(":")[0]),
                                                          int(x.Start.split(":")[1])
                                                          ), axis=1)
    df["id"] = df.apply(lambda x: x.StartDt.strftime("%Y-%m-%dT%H%M"), axis=1)

    df["StartHour"] = df["Start"].map(lambda x: int(x.split(":")[0]))

    with open("core/features.yaml") as fd: 
        features = yaml.safe_load(fd).get("Features")

    for name, feature_dict in features:
        func_name = feature_dict["func"]
        func = vars(ff)[func_name]
        df[name] = func(df)

    return df

