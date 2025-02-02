import pandas as pd

DATA_PATH = "/scratch/project/hackathon/data/SnowpackPredictionChallenge/input_data"

if __name__ == "__main__":
    part2_path = "part2.h5"
    swedata_path = f"{DATA_PATH}/swe_data/SWE_values_all.csv"
    mapping_path = "mapping.csv"

    print("processing data...")
    final_df = pd.DataFrame(pd.read_hdf(part2_path, key="key"))
    swe_df = pd.read_csv(swedata_path)
    swe_df = swe_df.rename(
        columns={
            "Date": "date",
            "SWE": "swe",
            "Latitude": "latitude",
            "Longitude": "longitude",
        }
    )
    map_df = pd.read_csv(mapping_path)

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
    swe_df[["latitude", "longitude"]] = swe_df.apply(
        lambda row: pd.Series(mapping(row)), axis=1
    )

    print("merging...")
    final_df = final_df.merge(swe_df, on=["date", "latitude", "longitude"], how="outer")

    # NOTE: filter out rows without a swe value
    print("filtering...")
    final_df = final_df.dropna(subset=["swe"])

    print("saving results (h5)...")
    final_df.to_hdf("data.h5", key="key", mode="w")

    print("saving results (csv)...")
    final_df.to_csv("data.csv")

    print(final_df)
    print(final_df["swe"].isna().sum())
