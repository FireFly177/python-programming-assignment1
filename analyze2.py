import pandas as pd
import numpy as np

# Read the merged CSV file
df = pd.read_csv("./data/merged_premier_league_stats.csv")

# Replace all instances of 'N/a' with actual NaN (Not a Number)
df.replace('N/a', np.nan, inplace=True)

# List of columns to exclude from numeric conversion
exclude_cols = ['Player', 'Nation', 'Pos', 'Squad']

# Convert all potential numeric columns to numeric, excluding the specified columns
for col in df.columns:
    if df[col].dtype == 'object' and col not in exclude_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Identify numeric columns (potential statistics)
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Exclude certain columns that might not be relevant statistics
stats_cols = [col for col in numeric_cols if col not in exclude_cols]

# Initialize a list to store results
results = []

# Calculate overall statistics
overall_stats = df[stats_cols].agg(['median', 'mean', 'std']).T
overall_stats.reset_index(inplace=True)
overall_stats.columns = ['Attribute', 'Median of Attribute 1', 'Mean of Attribute 1', 'Std of Attribute 1']
results.append(['All'] + overall_stats[['Median of Attribute 1', 'Mean of Attribute 1', 'Std of Attribute 1']].values.flatten().tolist())

# Calculate team-wise statistics
team_stats = df.groupby('Squad')[stats_cols].agg(['median', 'mean', 'std']).reset_index()
team_stats.columns = ['Team'] + [f'{stat} {metric}' for stat, metric in team_stats.columns[1:]]

# Append each team's statistics to results
for _, row in team_stats.iterrows():
    team_row = [row['Team']]
    for stat in stats_cols:
        team_row.extend(row[[f'{stat} median', f'{stat} mean', f'{stat} std']].values.flatten().tolist())
    results.append(team_row)

# Create DataFrame from results
num_attributes = len(stats_cols)
# Generate column names
columns = ['Team'] + [f'{stat} {metric}' for stat in stats_cols for metric in ['Median', 'Mean', 'Std']]
final_stats_df = pd.DataFrame(results, columns=columns)

# Add an index column starting from 1
final_stats_df.index += 1

# Save to CSV
final_stats_df.to_csv('./data/team_stats_analysis.csv', index=True)
final_stats_df.to_csv('./data/results2.csv', index=True)

print("Results have been saved to 'team_stats_analysis'")

# Display the first few rows of the result
print(final_stats_df)
