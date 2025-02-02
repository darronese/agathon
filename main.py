import csv
import numpy as np
import pandas as pd
from functools import reduce
import glob
# import tensorflow as tf
import matplotlib.pyplot as plt

files = {
    "/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/meteorological_data/Modified_Output_precip.csv" : "precip",
    "/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/meteorological_data/Modified_Output_Rmax.csv" : "Rmax",
    "/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/meteorological_data/Modified_Output_Rmin.csv" : "Rmin",
    "/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/meteorological_data/Modified_Output_SPH.csv" : "sph",
    "/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/meteorological_data/Modified_Output_SRAD.csv" : "srad",
    "/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/meteorological_data/Modified_Output_tmax.csv" : "tmax",
    "/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/meteorological_data/Modified_Output_tmin.csv" : "tmin",
    "/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/meteorological_data/Modified_Output_windspeed.csv" : "windspeed"
}

# Output file at TotalData.csv
output_file = "TotalData.csv"

# Merging all meteorological_data csvs into TotalData.csv
list = ['date','lat','lon']

dfs = []

for file, col in files.items():
    df1 = pd.read_csv(file)
    df1.rename(columns = {'variable_value' : col}, inplace=True)
    dfs.append(df1)

merged_df = dfs[0]
for df in dfs:
    merged_df = pd.merge(merged_df, df, on=list, how='outer')

merged_df.rename(columns = {'precip_y': 'precip'}, inplace=True)
del merged_df["precip_x"]
merged_df.to_csv(output_file, index=False)

'''
# Sort output file
df = pd.read_csv(output_file)
df = df.sort_values(by="date")
df.to_csv(output_file, index=False)
'''

# Fill in empty values using backward filling
df = pd.read_csv(output_file)
emptyVals = ['precip', 'Rmax', 'Rmin', 'sph', 'srad', 'tmax', 'tmin', 'windspeed']
for col in emptyVals:
    df[col] = df[col].bfill()

df.to_csv(output_file, index=False)






