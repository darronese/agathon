import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_swe_graphs(selected_date, csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Assuming 'Date' column exists and is in the format mm/dd/yyyy
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # Filter data based on the selected date
    df_filtered = df[df['Date'].dt.strftime('%m/%d/%Y') == selected_date]

    if not df_filtered.empty:
        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(df_filtered['Time'], df_filtered['Snowpack'], label='Snowpack')
        plt.xlabel('Time')
        plt.ylabel('Snowpack')
        plt.title(f'Snowpack for {selected_date}')
        plt.legend()
        plt.show()


# Example usage when imported into another script:
# generate_swe_graphs(year_to_filter=1991)