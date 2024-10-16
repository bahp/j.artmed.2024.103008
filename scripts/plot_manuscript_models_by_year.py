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
	'Tags': 'tags',
	'Methods': 'methods'
})

# Keep only interesting columns
df = df[['year', 'tags', 'methods']]
df = df.dropna(how='any')

# Ensure proper types
df.year = df.year.astype(int)
df.tags = df.tags.astype(str)



# ----------------------------
# From methods column
# ----------------------------
# Function to count occurrences for each group
def count_group_entries(item_string, groups):
	"""
	"""
	# Initialize a dictionary to hold counts for each group
	group_counts = {
		group_name: 0 for group_name in groups.keys()
	}

	# Check each group in the dictionary
	for group_name, group_values in groups.items():
		for value in group_values:
			if value.lower() in item_string.lower():
				group_counts[group_name] += 1  

	return group_counts  


groups = {
	'SCORES': ['SIRS', 'SOFA', 'qSOFA', 'MEWS', 'NEWS'],
	'RULE': ['PCT', 'PSEP', 'Rule'],
	'STATIC': ['RFC', 'LGBM', 'DTC', 'LGBM', 'XGB', 'Insight'],
	'TS_NOSEQ': ['ANN', 'DFN', 'CNN'],
	'TS_SEQ': ['ATTN', 'GRU', 'LSTM', 'RNN']
}

# Count for each category
df_counts = df['methods'] \
	.apply(count_group_entries, args=(groups,)) \
	.apply(pd.Series)


# Combine the original DataFrame with the group counts DataFrame
df_result = pd.concat([df, df_counts], axis=1)


# Group by 'Year' and sum the counts for each category
df_grouped = df_result \
	.drop(columns=['tags', 'methods']) \
	.groupby('year').sum()

# Create a stacked bar plot
df_grouped.plot(kind='bar', stacked=True)

# Add labels and title
plt.title('Total count per year for each Category')
plt.xlabel('Year')
plt.ylabel('Total Count')
plt.legend(title='Categories')

# Show plot
plt.xticks(rotation=90)  # Keep x-axis labels horizontal
plt.tight_layout()       # Adjust layout to make room for labels
plt.savefig("%s.png" % Path(__file__).stem, dpi=300)


# ----------------------------
# From tags column
# ----------------------------

REMOVE = [
	'timeseries', 'arxiv', 'Predictors', 'PhD', 
	'TEST', 'NLP', 'SERA', 'MGP', 'TPF', 'ENR'
]

groups1 = {
    'STATIC': [
    	'RFC', 'LGBM', 'DTC', 'LGBM', 'XGB', 
    	'Insight', 'LSVM', 'LR', 'SVM', 'GNB', 'RLR'
    ],
    'TS_NOSEQ': ['ANN', 'DFN', 'CNN', 'MLP', 'FNN'],
    'TS_SEQ': ['GRU', 'LSTM', 'RNN'],
    'RULE': ['PCT', 'PSEP', 'Rule']
}



# Function to assign group names based on the value
def assign_group(value, groups):
    for group_name, group_values in groups.items():
        if value in group_values:
            return group_name
    return value
    return 'Other'  # Default group if not found


# Step 1: Format and explode
df.tags = df.tags.str.replace(r'\s+', '', regex=True) \
	.str.replace('|', ',', regex=False) \
	.str.split(",").explode('tags') 

# Step 2: Remove not useful tags
df = df[~df.tags.isin(REMOVE)]

# Step 3: Group
df['group'] = df.tags.apply(assign_group, args=(groups,))

# ---------------------
# Display pandas
# ---------------------
# Group by 'Year' and 'Type' and count occurrences
df_counts = df.groupby(['year', 'group']).size().unstack(fill_value=0)

# Create stacked bar plot
df_counts.plot(kind='bar', stacked=True)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Number of manuscripts (by model/approach) over the years')
plt.legend(title='Type')
plt.xticks(rotation=90)  # Rotate x-axis labels if needed

# Show plot
plt.show()
