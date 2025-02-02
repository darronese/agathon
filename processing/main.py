import pandas as pd
import glob
import os

DATA_PATH = "/scratch/project/hackathon/data/SnowpackPredictionChallenge/input_data/"


"""
chatgpt prompt:
I have multiple CSV files containing 4 columns: date, latitude, longitude, and some 4th variable (temperature, wind speed, etc.)

There are missing values between my CSV files, in that a row with (date, latitude, longitude) in file 1 may not exist in file 2. The data is also not sorted.

How can I detect these missing values using Pandas?
"""
# requires a lot of memory


def find_missing_values(dfs):
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = merged_df.merge(df, on=["date", "lat", "lon"], how="outer")

    missing_values = merged_df.isnull().sum()

    print(missing_values)


# https://www.geeksforgeeks.org/working-with-missing-data-in-pandas/
# found no missing values
def find_empty_cells(df):
    return df.isnull().sum()


# found no missing dates
def find_missing_dates(df):
    df = df.set_index("date")
    df.index = pd.to_datetime(df.index)
    return pd.date_range(start="1990-01-01", end="2019-12-31").difference(df.index)


def find_duplicate_dates(df):
    return [i for i, v in df["date"].value_counts().iteritems() if v > 1]


def path_to_column_name(path):
    basename = os.path.basename(path)
    filename, _ = os.path.splitext(basename)
    return filename


if __name__ == "__main__":
    csv_paths = glob.glob(f"{DATA_PATH}/meteorological_data/*.csv")

    dfs = []
    for path in csv_paths:
        df = pd.read_csv(path)
        df = df.rename(columns={"variable_value": path_to_column_name(path)})
        dfs.append(df)

    find_missing_values(dfs)
