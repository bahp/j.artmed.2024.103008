# Libraries
import pandas as pd 
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib import patheffects

# Enable XKCD mode (hand drawn style)
plt.xkcd()

# Set fallback font manually
plt.rcParams.update({
    'font.family': 'Comic Sans MS, DejaVu Sans, sans-serif'
})

# ---------------------------------------------
# Methods
# ---------------------------------------------
def apply_sketch_style(fig):
    """
    Applies sketch-like styling to a given Matplotlib figure.
    
    Parameters:
    - fig: Matplotlib figure object to style.
    """
    # Set sketch-like font
    plt.rcParams["font.family"] = "Comic Sans MS"
    
    # Set background color for figure and axes
    fig.patch.set_facecolor('#f8f4e3')
    
    # Apply style to all axes in the figure
    for ax in fig.get_axes():
        # Set background color for axes
        ax.set_facecolor('#f8f4e3')
        
        # Add grid with light pencil color
        ax.grid(True, color='gray', linestyle=':', linewidth=0.5, alpha=0.5)
        
        # Style for axis labels and title
        for item in [ax.title, ax.xaxis.label, ax.yaxis.label]:
            item.set_path_effects([patheffects.withStroke(linewidth=1.5, foreground="white")])
            item.set_color('black')
        
        # Style for tick labels
        for tick in ax.get_xticklabels() + ax.get_yticklabels():
            tick.set_color('black')
            tick.set_path_effects([patheffects.withStroke(linewidth=1.5, foreground="white")])
        
        # Apply path effects to lines and bars (to all artist elements)
        for line in ax.get_lines() + ax.patches:
            line.set_path_effects([patheffects.withStroke(linewidth=3, foreground="white")])
            
    # Redraw the figure to apply changes
    fig.canvas.draw()



# ---------------------
# Load data
# ---------------------
# path
path = '../material/supplementary-material.xlsx'

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
df = df[~df.criteria.isin(['Mortality'])]

# Format the rest of categories
df.criteria = df.criteria.str.replace(
	r'.*Septic Shock.*', 'Septic Shock', case=False, regex=True)
df.criteria = df.criteria.str.replace(
	r'.*sepsis.*', 'Sepsis', case=False, regex=True)
df.criteria = df.criteria.str.replace(
	r'.*bacteremia.*', 'Bacteremia', case=False, regex=True)
df.criteria = df.criteria.replace({
	'Positive culture': 'Bacteremia',
	'Infection': 'BSI',
	'Sepsis\nSeptic Shock': 'Sepsis'
})


# ---------------------
# Display pandas
# ---------------------
# Group by 'Year' and 'Type' and count occurrences
df_counts = df.groupby(['year', 'criteria']) \
	.size().unstack(fill_value=0)

# Create stacked bar plot
df_counts.plot(kind='bar', stacked=True)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Number of manuscripts (by topic) over the years')
plt.legend(title='Type')
plt.xticks(rotation=90)  # Rotate x-axis labels if needed

# Apply the sketch style
#apply_sketch_style(plt.gcf())

# Adjust
plt.tight_layout()

# Save
plt.savefig("%s.png" % Path(__file__).stem, dpi=300)

# Show plot
plt.show()