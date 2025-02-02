import pandas as pd

if __name__ == "__main__":
    print("processing data...")
    df = pd.read_csv("../input_data/data.csv")

    print("filtering out summer dates...")
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"].dt.month >= 12) | (df["date"].dt.month <= 5)]

    df.to_csv("winter_data.csv", index=False)
