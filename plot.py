import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("./data/merged_premier_league_stats.csv")

# Replace 'N/a' with NaN
df.replace('N/a', np.nan, inplace=True)

# List of columns to exclude from numeric conversion and plotting
exclude_cols = ['Player', 'Nation', 'Pos', 'Squad']

# Convert appropriate columns to numeric
for col in df.columns:
    if df[col].dtype == 'object' and col not in exclude_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Identify numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Remove slashes and colons from numeric column names for safety
safe_numeric_cols = [stat.replace('/', '').replace(':', '') for stat in numeric_cols]

# Add a 'Team' column where 'All Players' will represent the entire dataset
df['Team'] = df['Squad']
df_all_players = df.copy()
df_all_players['Team'] = 'All Players'

# Combine data (all players + each team)
df_combined = pd.concat([df, df_all_players])

# Create 'histograms' directory if it doesn't exist
if not os.path.exists('histograms'):
    os.makedirs('histograms')

# Ensure that numeric_cols is used for looping over statistics
for stat in numeric_cols:
    plt.figure(figsize=(12, 8))

    # Calculate mean for each team, excluding NaNs
    team_stats = df_combined.groupby('Team')[stat].mean().reset_index()

    # Create a bar plot for the stat with color representing teams
    sns.barplot(data=team_stats, x='Team', y=stat, hue='Team', palette='Set2', errorbar=None, legend=False)

    # Add title and labels
    plt.title(f"Mean {stat} for All Players and Each Team", fontsize=16)
    plt.xlabel("Team", fontsize=14)
    plt.ylabel(stat, fontsize=14)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=90)

    # Save the figure to the 'histograms' folder
    safe_stat_name = stat.replace('/', '').replace(':', '')  # Safe for file names
    plt.savefig(f'histograms/{safe_stat_name}_mean_barplot.png', bbox_inches='tight', dpi=300)
    print(f"Saved bar plot for {stat}")

    # Close the plot to free memory
    plt.close()

print("All bar plots have been saved to the 'histograms' folder.")
