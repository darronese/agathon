import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox
from pathlib import Path

def plot_swe(df, latitude, longitude, date):
    """
    Plots the SWE data for a given latitude, longitude, and year.
    If no data is found for the selected date, it will return an alert box with specific error messages.
    """
    try:
        # Convert selected_date to integer (to match DataFrame type)
        date = int(date)

        # Normalize column names to lowercase to handle case-sensitivity issues
        df.columns = df.columns.str.strip().str.lower()

        # Ensure 'date' is in datetime format
        if 'date' not in df.columns:
            messagebox.showerror("Error", "The CSV file does not contain a 'date' column.")
            return
        
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Extract year directly from the 'date' column
        df['year'] = df['date'].dt.year

        # Filter data by the selected year
        df_filtered_year = df[df['year'] == date].copy()  # Avoid SettingWithCopyWarning

        if df_filtered_year.empty:
            messagebox.showerror("Error", f"No data found for the year {date}.")
            return

        # Aggregate SWE data by month (average for each month)
        df_filtered_year['month'] = df_filtered_year['date'].dt.month
        df_monthly = df_filtered_year.groupby('month')['swe'].mean()

        # Create a list of months (1-12) to ensure all months are represented
        months = list(range(1, 13))
        swe_values = [df_monthly.get(month, 0) for month in months]  # Default to 0 if month missing

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(months, swe_values, marker='o', linestyle='-', color='b')
        plt.title(f"Monthly SWE for {latitude} / {longitude} - {date}")
        plt.xlabel("Month")
        plt.ylabel("SWE (Snow Water Equivalent)")
        plt.xticks(months, ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

        # Show the plot
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def fetch_data_and_plot(latitude, longitude, date):
    """
    Fetches the data from the CSV file and plots the SWE data for a given latitude, longitude, and year.
    
    :param latitude: Latitude of the location
    :param longitude: Longitude of the location
    :param date: Year for which to plot the SWE data
    """
    try:
        # Construct the file name based on latitude and longitude
        lat_str = f"lat_{latitude.replace('.', '_')}"
        lon_str = f"lon_{longitude.replace('.', '_')}"
        file_name = f"{lat_str}_{lon_str}.csv"
        
        # Define the directory where CSV files are stored
        OUTPUT_CSV_PATH = Path(__file__).parent / "output_csv"
        
        # Construct the full file path
        file_path = OUTPUT_CSV_PATH / file_name
        
        # Check if the file exists
        if not file_path.exists():
            messagebox.showerror("Error", f"No Lat/Lon/Date input or File '{file_name}' not found!")
            return
        
        # Read the CSV data
        df = pd.read_csv(file_path)

        # Normalize column names to lowercase to handle case-sensitivity issues
        df.columns = df.columns.str.strip().str.lower()

        # Ensure the 'date' column is in datetime format
        if 'date' not in df.columns:
            messagebox.showerror("Error", "The CSV file does not contain a 'date' column.")
            return

        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Filter the data based on latitude and longitude
        df_filtered = df[(df['latitude'] == float(latitude)) & 
                         (df['longitude'] == float(longitude))]

        # Call the plot_swe function to plot the data
        plot_swe(df_filtered, latitude, longitude, date)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
