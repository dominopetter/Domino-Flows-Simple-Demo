import os
import pandas as pd

# Read inputs
named_input_1 = "datasetA"
datasetA_path = "/workflow/inputs/{}".format(named_input_1)

named_input_2 = "datasetB"
datasetB_path = "/workflow/inputs/{}".format(named_input_2)

# Load data
a = pd.read_csv(datasetA_path, index_col='Id') 
b = pd.read_csv(datasetB_path, index_col='Id') 

# Merge data
print('Merging data...')
merged = pd.concat([a, a], axis=0).reset_index(drop=True)
print(merged)

# Write output
merged.to_csv('/workflow/outputs/merged_data.csv', index=False)
