import csv
import numpy as np
import pandas as pd

df = pd.read_csv('/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/swe_data/SWE_values_all.csv')

min_latitude = df['Latitude'].min()
max_latitude = df['Latitude'].max()
min_longitude = df['Longitude'].min()
max_longitude = df['Longitude'].max()

print("Min Latitude: ", min_latitude) # 33.65352
print("Max Latitude: ", max_latitude) # 48.97523
print("Min Longitude: ", min_longitude) # -123.37315
print("Max Longitude: ", max_longitude) # -103.97688
