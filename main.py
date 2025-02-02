import csv
import numpy as np
import pandas as pd
from functools import reduce
import glob
# import tensorflow as tf
import matplotlib.pyplot as plt

'''
df = pd.read_csv('/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/swe_data/SWE_values_all.csv')

min_latitude = df['Latitude'].min()
max_latitude = df['Latitude'].max()
min_longitude = df['Longitude'].min()
max_longitude = df['Longitude'].max()

print("Min Latitude: ", min_latitude) # 33.65352
print("Max Latitude: ", max_latitude) # 48.97523
print("Min Longitude: ", min_longitude) # -123.37315
print("Max Longitude: ", max_longitude) # -103.97688
'''

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

for file, col in files.items():
    '''
    # Sort values by date in each file
    df = pd.read_csv(file)
    df = df.sort_values(by="date")
    df.to_csv(file, index=False)
    '''
    df1 = pd.read_csv(file)
    df2 = pd.read_csv(output_file)

    list = ['date','lat','lon']

    merged_df = df2.merge(df1, on=list, how='outer')
    merged_df.rename(columns = {'variable_value': col}, inplace=True)
    merged_df = merged_df.loc[:, ~merged_df.columns.str.contains('^Unnamed')]
    merged_df.to_csv(output_file, index=False)


'''
# Copy SWE_values_all.csv to TotalData.csv
swe = "/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/swe_data/SWE_values_all.csv"

with open (swe, "r", newline='') as src, open(output_file, "w", newline='') as dest:
    reader = csv.reader(src)
    writer = csv.writer(dest)
    # header = ["date","SWE","lat","lon","precip","rmax","rmin","sph","srad","tmax","tmin","windspeed"]
    header = ["date","SWE","lat","lon",""]
    writer.writerow(header)
    next(reader)
    for row in reader:
        row.append("")
        writer.writerow(row)

# Sort output file
df = pd.read_csv(output_file)
df = df.sort_values(by="date")
df.to_csv(output_file, index=False)

# Copy Modified_Output_precip.csv precip values and merge them with TotalData.csv
precip = "/Users/sairaghavgubba/Desktop/AgATHON 2025/input_data/meteorological_data/Modified_Output_precip.csv";

# Sort values by date in precip csv
df1 = pd.read_csv(precip)
df1 = df1.sort_values(by="date")
df1.to_csv(precip, index=False)


precip_df = pd.read_csv(precip)
total_df = pd.read_csv(output_file)

merged_df = pd.merge(total_df, precip_df[["date", "lat", "lon", "variable_value"]], on=["date", "lat", "lon"], how='left')

merged_df.rename(columns = {'variable_value': 'precip'}, inplace=True)
merged_df = merged_df.loc[:, ~total_df.columns.str.contains('^Unnamed')]

merged_df.to_csv(output_file, index=False)


with open (precip, "r", newline='') as src, open(output_file, "r", newline='') as dest:
        reader1 = csv.reader(src) # precip file
        reader2 = csv.reader(dest) # output file
        rows1 = list(reader1)[1:]
        rows2 = list(reader2)[1:]

        merged_rows = []

        for row1 in rows1:
            match_found = False
            for row2 in rows2:
                if (row1[0] == row2[0] and row1[1] == row2[2] and row1[2] == row2[3]):
                   row2.append(row1[3])
                   row2.append("")
                   match_found = True
                   merged_rows.append(row2)
                   break
            if not match_found:
                new_row = [row1[0], "", row1[1], row1[2], row1[3],""]
                merged_rows.append(new_row)

with open(output_file, "w", newline='') as dest1:
    writer = csv.writer(dest1)
    header = ["date", "SWE", "lat", "lon", "precip", "rmax", "rmin", "sph", "srad", "tmax", "tmin", "windspeed"]
    writer.writerow(header)
    writer.writerows(merged_rows)
'''





