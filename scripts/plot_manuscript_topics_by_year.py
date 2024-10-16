# Libraries
import pandas as pd 
import matplotlib.pyplot as plt
from pathlib import Path

path = '../material/supplementary-material.xlsx'


# ---------------------
# Load data
# ---------------------
# Load data
df = pd.read_excel(io=path, 
	sheet_name='STUDIES', engine='openpyxl',
	header=0)

# Rename columns
df = df.rename(columns={
	'Year': 'year',
	'Positive criteria (smmry)': 'criteria'
})

# Keep only interesting columns
df = df[['year', 'criteria']]
df = df.dropna(how='any')

# Ensure proper types
df.year = df.year.astype(int)
df.criteria = df.criteria.astype(str)

# Remove some not useful categories
df = df[~df.criteria.isin(['Mortality', 'Septic Shock'])]

# Format the rest of categories
df.criteria = df.criteria.str.replace(r'.*sepsis.*', 'Sepsis', case=False, regex=True)
df.criteria = df.criteria.str.replace(r'.*bacteremia.*', 'Bacteremia', case=False, regex=True)
df.criteria = df.criteria.replace({
	'Positive culture': 'Bacteremia',
	'Infection': 'BSI',
	})


# Show
print(df)


# ---------------------
# Display pandas
# ---------------------
# Group by 'Year' and 'Type' and count occurrences
df_counts = df.groupby(['year', 'criteria']).size().unstack(fill_value=0)

# Create stacked bar plot
df_counts.plot(kind='bar', stacked=True)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Number of manuscripts (by topic) over the years')
plt.legend(title='Type')
plt.xticks(rotation=90)  # Rotate x-axis labels if needed

plt.savefig("%s.png" % Path(__file__).stem, dpi=300)

# Show plot
plt.show()
