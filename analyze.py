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

# Identify non-numeric columns after the conversion
non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
print("Non-numeric columns:", non_numeric_cols)

# Function to get top and bottom 3 players for a statistic
def get_top_bottom_players(df, stat):
    # Sort values in descending order for top 3, skipping NaN values
    top_3 = df.nlargest(3, stat)[['Player', 'Squad', stat]]
    # Sort values in ascending order for bottom 3, skipping NaN values
    bottom_3 = df.nsmallest(3, stat)[['Player', 'Squad', stat]]
    return top_3, bottom_3

# Identify numeric columns (potential statistics)
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Exclude certain columns that might not be relevant statistics
stats_cols = [col for col in numeric_cols if col not in exclude_cols]

# Dictionary to store results
results = {}

# Analyze each statistic
for stat in stats_cols:
    # Skip columns with all NaN values
    if df[stat].isna().all():
        continue
    
    # Get top and bottom 3 players
    top_3, bottom_3 = get_top_bottom_players(df, stat)
    
    results[stat] = {
        'top_3': top_3.to_dict('records'),
        'bottom_3': bottom_3.to_dict('records')
    }

# Prepare data for CSV in the desired format
output_rows = []
for stat, data in results.items():
    # Add top 3 players
    for i in range(3):
        output_rows.append({
            'Statistic': stat,
            'Rank': f'Top {i+1}',
            'Player': data['top_3'][i]['Player'],
            'Squad': data['top_3'][i]['Squad'],
            'Value': data['top_3'][i][stat]
        })
    # Add bottom 3 players
    for i in range(3):
        output_rows.append({
            'Statistic': stat,
            'Rank': f'Bottom {i+1}',
            'Player': data['bottom_3'][i]['Player'],
            'Squad': data['bottom_3'][i]['Squad'],
            'Value': data['bottom_3'][i][stat]
        })

# Create DataFrame and save to CSV
output_df = pd.DataFrame(output_rows)
output_df.to_csv("./data/player_stats_analysis.csv", index=False)
print("\nDetailed results saved to 'player_stats_analysis.csv'")
