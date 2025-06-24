import os
import pandas as pd


# Read data input
named_input = "merged_data"
merged_data_path = "/workflow/inputs/{}".format(named_input)

# Load data
df = pd.read_csv(merged_data_path) 

# Process data
print(df)
print('Processing the data ...')
df = df.drop('RandomColumn', axis=1)
print(df)

# Write output
df.to_csv('/workflow/outputs/processed_data.csv', index=False)


