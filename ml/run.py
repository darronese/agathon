import pandas as pd
import matplotlib.pyplot as plt
import pickle

if __name__ == "__main__":
    print("processing data...")
    df = pd.read_csv("winter_data.csv", parse_dates=["date"])

    # NOTE: rfg cannot handle dates; convert to year and day
    df["day"] = df["date"].dt.dayofyear
    df["year"] = df["date"].dt.year

    X = df[
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
    y = df["swe"]

    with open("model.pkl", "rb") as f:
        rf = pickle.load(f)

    importances = rf.feature_importances_
    feature_names = X.columns

    plt.figure(figsize=(10, 5))
    plt.barh(feature_names, importances, color="purple")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.title("SWE Feature Importances")
    plt.show()

    first_10 = X.iloc[:10]
    print(first_10)

    print("predicting...")
    predictions = rf.predict(first_10)
    print(predictions)
