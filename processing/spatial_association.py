import pandas as pd
from scipy.spatial import cKDTree

DATA_PATH = "/scratch/project/hackathon/data/SnowpackPredictionChallenge/input_data"

if __name__ == "__main__":
    sidata_path = f"{DATA_PATH}/swe_data/Station_Info.csv"
    mdata_path = "m_data.h5"

    print("processing data...")
    si_df = pd.read_csv(sidata_path)
    si_df = si_df.rename(
        columns={
            "Station": "station",
            "Latitude": "latitude",
            "Longitude": "longitude",
        }
    )
    si_df = si_df.drop(columns=["Elevation", "Southness"])
    m_df = pd.DataFrame(pd.read_hdf(mdata_path, key="key"))

    print("removing duplicates...")
    si_coords = (
        si_df[["latitude", "longitude"]].drop_duplicates().reset_index(drop=True)
    )
    m_coords = m_df[["latitude", "longitude"]].drop_duplicates().reset_index(drop=True)

    print("computing nearest neighbors...")
    tree = cKDTree(m_coords[["latitude", "longitude"]])
    _, idx = tree.query(si_coords[["latitude", "longitude"]])
    matched = m_coords.iloc[idx].reset_index(drop=True)

    print("merging...")
    map_df = si_coords.copy()
    map_df["matched_latitude"] = matched["latitude"].values
    map_df["matched_longitude"] = matched["longitude"].values

    print("creating mapping...")
    si_to_m = {
        (row["latitude"], row["longitude"]): (
            row["matched_latitude"],
            row["matched_longitude"],
        )
        for _, row in map_df.iterrows()
    }

    def mapping(row):
        return si_to_m[(row["latitude"], row["longitude"])]

    print("mapping coordinates...")
    si_df[["latitude", "longitude"]] = si_df.apply(
        lambda row: pd.Series(mapping(row)), axis=1
    )

    print("filtering meteorological data...")
    m_df = m_df.merge(si_df, on=["latitude", "longitude"], how="inner")

    print("saving results...")
    si_df.to_csv("spatial.csv", index=False)
    m_df.to_hdf("filtered_m_data.hd5", key="key", mode="w")
