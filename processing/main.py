import pandas as pd
import glob
import os
from scipy.spatial import cKDTree

DATA_PATH = "/scratch/project/hackathon/data/SnowpackPredictionChallenge/input_data/"


"""
chatgpt prompt:
I have multiple CSV files containing 4 columns: date, latitude, longitude, and some 4th variable (temperature, wind speed, etc.)

There are missing values between my CSV files, in that a row with (date, latitude, longitude) in file 1 may not exist in file 2. The data is also not sorted.

How can I detect these missing values using Pandas?
"""
# NOTE: requires a lot of memory


def path_to_column_name(path):
    basename = os.path.basename(path)
    filename, _ = os.path.splitext(basename)
    return filename


if __name__ == "__main__":
    swedata_path = f"{DATA_PATH}/swe_data/SWE_values_all.csv"
    mdata_paths = glob.glob(f"{DATA_PATH}/meteorological_data/*.csv")
    sidata_path = f"{DATA_PATH}/swe_data/Station_Info.csv"

    print("processing swe data...")
    swe_df = pd.read_csv(swedata_path)
    swe_df = swe_df.rename(
        columns={
            "Date": "date",
            "SWE": "swe",
            "Latitude": "latitude",
            "Longitude": "longitude",
        }
    )
    swe_df = swe_df[["date", "latitude", "longitude", "swe"]]

    print("processing station data...")
    si_df = pd.read_csv(sidata_path)
    si_df = si_df.drop(columns=["Station"])
    si_df = si_df.rename(
        columns={
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Elevation": "elevation",
            "Southness": "southness",
        }
    )
    swe_df = swe_df.merge(si_df, on=["latitude", "longitude"], how="outer")

    print("processing meteorological data...")
    m_dfs = []
    for path in mdata_paths:
        si_df = pd.read_csv(path)
        si_df = si_df.rename(
            columns={
                "lat": "latitude",
                "lon": "longitude",
                "variable_value": path_to_column_name(path)[16:].lower(),
            }
        )
        m_dfs.append(si_df)
    m_df = pd.concat(m_dfs, ignore_index=True)

    print("mapping coordinates...")
    swe_coords = swe_df[["latitude", "longitude"]].drop_duplicates().to_numpy()
    m_coords = m_df[["latitude", "longitude"]].drop_duplicates().to_numpy()

    tree = cKDTree(m_coords)
    _, nearest_idx = tree.query(swe_coords)
    matched = m_df.iloc[nearest_idx].reset_index(drop=True)
    coord_mapping = dict(
        zip(
            [tuple(coord) for coord in swe_coords],
            [tuple(coord) for coord in matched[["latitude", "longitude"]].to_numpy()],
        )
    )

    def transform_coords(row, mapping):
        return mapping.get(
            (row["latitude"], row["longitude"]), (row["latitude"], row["longitude"])
        )

    print("transforming...")
    swe_df[["latitude", "longitude"]] = swe_df.apply(
        transform_coords, axis=1, mapping=coord_mapping, result_type="expand"
    )

    print("merging...")
    res = pd.merge(m_df, swe_df, on=["date", "latitude", "longitude"], how="left")
    res.to_csv("data1.csv", index=False)

    """
    # locate nearest coords for swe values
    tree = cKDTree(m_df[["latitude", "longitude"]].to_numpy())
    _, nearest_idx = tree.query(swe_df[["latitude", "longitude"]].to_numpy())
    matched = m_df.iloc[nearest_idx].reset_index(drop=True)
    res_df = swe_df.copy()
    res_df["matched_latitude"] = matched["latitude"]
    res_df["matched_longitude"] = matched["longitude"]
    res_df = res_df.merge(
        m_df,
        left_on=["date, matched_latitude, matched_longitude"],
        right_on=["date", "latitude", "longitude"],
        how="left",
    )
    res_df = res_df.drop(columns=["latitude", "longitude"])
    res_df = res_df.rename(
        columns={
            "matched_latitude": "latitude",
            "matched_longitude": "longitude",
        }
    )

    res_df.to_csv("data1.csv", index=False)
    """

"""
# https://www.geeksforgeeks.org/working-with-missing-data-in-pandas/
# found no missing values
def find_empty_cells(df):
    return df.isnull().sum()


# found no missing dates
def find_missing_dates(df):
    df = df.set_index("date")
    df.index = pd.to_datetime(df.index)
    return pd.date_range(start="1990-01-01", end="2019-12-31").difference(df.index)


# found duplicate dates; realised this is expected
def find_duplicate_dates(df):
    return [i for i, v in df["date"].value_counts().iteritems() if v > 1]
"""
