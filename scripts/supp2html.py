import pandas as pd

# Path
path = '../material/supplementary-material.xlsx'

# Load
df = pd.read_excel(path, sheet_name='STUDIES')

print(df)

df.to_json('records.json', orient='records', indent=4)