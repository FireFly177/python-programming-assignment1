import pandas as pd
import os

# List of CSV files to be merged (excluding the base file)
csv_files = [
    "./data/premier_league_standard_stats.csv",  # Base file
    "./data/premier_league_goalkeeping_stats.csv",
    "./data/premier_league_shooting_stats.csv",
    "./data/premier_league_passing_stats.csv",
    "./data/premier_league_pass_types_stats.csv",
    "./data/premier_league_goal_and_shot_creation_stats.csv",
    "./data/premier_league_defensive_actions_stats.csv",
    "./data/premier_league_possession_stats.csv",
    "./data/premier_league_playing_time_stats.csv",
    "./data/premier_league_miscellaneous_stats.csv"
]

# Function to read CSV files
def read_csv(file):
    return pd.read_csv(file)

# Read the standard stats file as the base dataframe
base_df = read_csv("./data/premier_league_standard_stats.csv")

# Merge other dataframes onto the base dataframe, skipping the first file (base)
for file in csv_files[1:]:  # Start from the second file in the list
    if os.path.exists(file):
        df = read_csv(file)
        
        # Merge based on 'Player', 'Pos', and 'Squad'
        # Using left join to keep all rows from the base dataframe
        base_df = pd.merge(base_df, df, on=['Player', 'Pos', 'Squad'], how='left', suffixes=('', '_y'))
        
        # Drop columns with '_y' suffix, as they are duplicates
        base_df = base_df.loc[:, ~base_df.columns.str.endswith('_y')]

# Replace missing statistics (NaN) with "N/a"
base_df = base_df.fillna('N/a')
base_df = base_df.drop(columns=['Rk', 'Matches'], errors='ignore')

# Ensure 'Playing Time-Min' is numeric and coerce any errors to NaN
# First, remove commas if they exist, then convert to numeric
base_df['Playing Time-Min'] = base_df['Playing Time-Min'].replace({',': ''}, regex=True)
base_df['Playing Time-Min'] = pd.to_numeric(base_df['Playing Time-Min'], errors='coerce')

# Filter players who have played more than 90 minutes in the season
filtered_df = base_df[base_df['Playing Time-Min'] > 90]

# Sort by player name and, in case of a tie, by age (oldest first)
# Assuming 'Age' column exists. Adjust this if necessary.
sorted_df = filtered_df.sort_values(by=['Player', 'Age'], ascending=[True, False])

# Print the sorted and filtered dataframe information
print(f"Filtered and sorted data:")
print(sorted_df.head())  # Display the top rows of the result
print(f"\nTotal number of rows after filtering: {len(sorted_df)}")
print(f"Total number of columns: {len(sorted_df.columns)}")

# Save the merged, filtered, and sorted DataFrame to a new CSV file
sorted_df.to_csv("./data/merged_premier_league_stats.csv", index=False)
# sorted_df.to_excel("./data/merged_premier_league_stats.xlsx", index=False)
sorted_df.to_csv("./data/result.csv", index=False)
