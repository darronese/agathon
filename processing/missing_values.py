import pandas as pd
import glob
import os

DATA_PATH = "/scratch/project/hackathon/data/SnowpackPredictionChallenge/input_data"


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
    m_cols = []
    m_dfs = []
    for i, path in enumerate(mdata_paths):
        colname = path_to_column_name(path)[16:].lower()
        print(f"processing {colname} data... ({i + 1}/{len(mdata_paths)})")
        df = pd.read_csv(path)
        df = df.rename(
            columns={"lat": "latitude", "lon": "longitude", "variable_value": colname}
        )
        m_cols.append(colname)
        m_dfs.append(df)

    m_df = m_dfs[0]
    for df in m_dfs[1:]:
        m_df = m_df.merge(df, on=["date", "latitude", "longitude"], how="outer")

    print("performing mean imputation...")
    for i, col in enumerate(m_cols):
        print(f"imputing {col}... ({i + 1}/{len(m_cols)})")
        mean = m_df[col].mean()
        m_df[col] = m_df[col].fillna(mean)

    print("saving results...")
    swe_df.to_hdf("swe_data.h5", key="key", mode="w")
    m_df.to_hdf("m_data.h5", key="key", mode="w")

    print(m_df)
