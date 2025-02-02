# separateCSV.py
import os
import pandas as pd
from pathlib import Path

def split_data_by_coordinates(input_csv):
    # Resolve input CSV path relative to script directory if necessary
    input_csv_path = Path(input_csv)

    # If the input CSV path is relative, resolve it relative to the script's directory
    if not input_csv_path.is_absolute():
        input_csv_path = Path(__file__).parent / input_csv_path

    # Check if the input CSV exists
    if not input_csv_path.exists():
        print(f"Error: The file {input_csv_path} does not exist.")
        return

    # Read the CSV file
    df = pd.read_csv(input_csv_path)

    # Clean up column names (convert to lowercase and remove spaces)
    df.columns = df.columns.str.strip().str.lower()

    # Check if 'date' column exists
    if 'date' not in df.columns:
        print("Error: The CSV file must contain a 'date' column.")
        print(f"Available columns: {df.columns}")
        return

    # Ensure 'date' is in datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Create the output directory for CSV files (relative to the script's location)
    output_csv_folder = Path(__file__).parent / "output_csv"
    output_csv_folder.mkdir(parents=True, exist_ok=True)  # Create folder if it doesn't exist

    # Group by unique (latitude, longitude) pairs and save them to different CSV files
    grouped = df.groupby(['latitude', 'longitude'])

    # Iterate through each group and save it in the output_csv folder
    for (lat, lon), group in grouped:
        # Sanitize the file name (replace spaces, commas, periods with underscores)
        file_name = f"lat_{lat}_lon_{lon}".replace(" ", "_").replace(",", "_").replace(".", "_")

        # Define the full file path for the CSV file in the output_csv folder
        output_file_path = output_csv_folder / f"{file_name}.csv"

        # Save the group to the CSV file
        group.to_csv(output_file_path, index=False)
        print(f"Saved data for Latitude {lat} and Longitude {lon} to {output_file_path}")

    # Notify user of success
    print("CSV processing complete.")
