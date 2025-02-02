import sys
import pandas as pd
import pickle

if __name__ == "__main__":
    dynamic_path = sys.argv[1]
    static_path = sys.argv[2]
    model_path = sys.argv[3]

    print("processing data...")
    d_df = pd.read_csv(dynamic_path, parse_dates=["date"])
    s_df = pd.read_csv(static_path)

    d_df = d_df.rename(
        columns={
            "lat": "latitude",
            "lon": "longitude",
            "Rmax": "rmax",
            "Rmin": "rmin",
            "SPH": "sph",
            "SRAD": "srad",
        }
    )
    s_df = s_df.rename(
        columns={
            "lat": "latitude",
            "lon": "longitude",
            "Elevation": "elevation",
            "Southness": "southness",
        }
    )

    df = d_df.merge(s_df, on=["latitude", "longitude"], how="outer")

    # NOTE: rfg cannot handle dates; convert to year and day
    df["day"] = df["date"].dt.dayofyear
    df["year"] = df["date"].dt.year

    df = df[
        [
            "year",
            "day",
            "latitude",
            "longitude",
            "precip",
            "tmin",
            "tmax",
            "sph",
            "srad",
            "rmax",
            "rmin",
            "windspeed",
            "elevation",
            "southness",
        ]
    ]

    print("predicting...")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    df["swe_prediction"] = model.predict(df)
    df["date"] = pd.to_datetime(
        df["year"].astype(str) + df["day"].astype(str), format="%Y%j"
    )
    df = df[["date", "latitude", "longitude", "swe_prediction"]]
    df.to_csv("predictions.csv", index=False)  # type: ignore
