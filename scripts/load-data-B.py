import os
import pandas as pd

# Read the location of the csv from the task input blob
input_name = "data_path"
input_location = f"/workflow/inputs/{input_name}"
with open(input_location, "r") as file:
    input_csv = file.read()

# Read input csv to dataframe
df = pd.read_csv(input_csv) 


# Write to Flow output
df.to_csv('/workflow/outputs/datasetB.csv', index=False)
