import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    df = pd.read_csv("predictions.csv", parse_dates=["date"])
    s_df = pd.read_csv("snotels.csv")

    _, axis = plt.subplots(2, 5)

    locs = df[["latitude", "longitude"]].drop_duplicates()
    for i, row in enumerate(locs.itertuples(index=False)):
        lat, lon = row.latitude, row.longitude  # type: ignore

        loc_name = s_df[
            (s_df.latitude == lat) & (s_df.longitude == lon)
        ].station.values[0]
        data = df[(df.latitude == lat) & (df.longitude == lon)]
        data = data[["date", "swe_prediction"]]

        row = i // 5
        col = i % 5
        axis[row, col].plot(data["date"], data["swe_prediction"])
        axis[row, col].set_title(loc_name)

    plt.show()
