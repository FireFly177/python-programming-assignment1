import pandas as pd

# Load the team statistics analysis CSV
final_stats_df = pd.read_csv('./data/team_stats_analysis.csv', index_col=0)

# List of statistics where higher is better
higher_is_better = [
    'Playing Time-MP Mean', 'Playing Time-Starts Mean', 'Playing Time-Min Mean', 
    'Playing Time-90s Mean', 'Performance-Gls Mean', 'Performance-Ast Mean', 
    'Performance-G+A Mean', 'Performance-G-PK Mean', 'Performance-PK Mean', 
    'Performance-PKatt Mean', 'Expected-xG Mean', 'Expected-npxG Mean', 
    'Expected-xAG Mean', 'Expected-npxG+xAG Mean', 'Progression-PrgC Mean', 
    'Progression-PrgP Mean', 'Progression-PrgR Mean', 'Per 90 Minutes-Gls Mean', 
    'Per 90 Minutes-Ast Mean', 'Per 90 Minutes-G+A Mean', 'Per 90 Minutes-G-PK Mean', 
    'Per 90 Minutes-G+A-PK Mean', 'Per 90 Minutes-xG Mean', 'Per 90 Minutes-xAG Mean', 
    'Per 90 Minutes-xG+xAG Mean', 'Per 90 Minutes-npxG Mean', 
    'Performance-GA Mean', 'Performance-GA90 Mean', 'Performance-SoTA Mean', 
    'Performance-Saves Mean', 'Performance-Save% Mean', 'Performance-W Mean', 
    'Performance-D Mean', 'Performance-L Mean', 'Performance-CS Mean', 
    'Performance-CS% Mean', 'Penalty Kicks-PKatt Mean', 'Penalty Kicks-PKA Mean', 
    'Penalty Kicks-PKsv Mean', 'Penalty Kicks-PKm Mean', 
    'Penalty Kicks-Save% Mean', '90s Mean', 'Standard-Gls Mean', 
    'Standard-Sh Mean', 'Standard-SoT Mean', 'Standard-SoT% Mean', 
    'Standard-Sh/90 Mean', 'Standard-SoT/90 Mean', 'Standard-G/Sh Mean', 
    'Standard-G/SoT Mean', 'Standard-Dist Mean', 'Standard-FK Mean', 
    'Standard-PK Mean', 'Standard-PKatt Mean', 'Expected-npxG/Sh Mean', 
    'Expected-G-xG Mean', 'Expected-np:G-xG Mean', 'Total-Cmp Mean', 
    'Total-Att Mean', 'Total-Cmp% Mean', 'Total-TotDist Mean', 
    'Total-PrgDist Mean', 'Short-Cmp Mean', 'Short-Att Mean', 
    'Short-Cmp% Mean', 'Medium-Cmp Mean', 'Medium-Att Mean', 
    'Medium-Cmp% Mean', 'Long-Cmp Mean', 'Long-Att Mean', 'Long-Cmp% Mean', 
    'Ast Mean', 'xAG Mean', 'Expected-xA Mean', 'Expected-A-xAG Mean', 
    'KP Mean', '1/3 Mean', 'PPA Mean', 'CrsPA Mean', 'PrgP Mean', 
    'Att Mean', 'Pass Types-Live Mean', 'Pass Types-Dead Mean', 
    'Pass Types-FK Mean', 'Pass Types-TB Mean', 'Pass Types-Sw Mean', 
    'Pass Types-Crs Mean', 'Pass Types-TI Mean', 'Pass Types-CK Mean', 
    'Corner Kicks-In Mean', 'Corner Kicks-Out Mean', 'Corner Kicks-Str Mean', 
    'Outcomes-Cmp Mean', 'Outcomes-Off Mean', 'Outcomes-Blocks Mean', 
    'SCA-SCA Mean', 'SCA-SCA90 Mean', 'SCA Types-PassLive Mean', 
    'SCA Types-PassDead Mean', 'SCA Types-TO Mean', 'SCA Types-Sh Mean', 
    'SCA Types-Fld Mean', 'SCA Types-Def Mean', 'GCA-GCA Mean', 
    'GCA-GCA90 Mean', 'GCA Types-PassLive Mean', 'GCA Types-PassDead Mean', 
    'GCA Types-TO Mean', 'GCA Types-Sh Mean', 'GCA Types-Fld Mean', 
    'GCA Types-Def Mean', 'Tackles-Tkl Mean', 'Tackles-TklW Mean', 
    'Tackles-Def 3rd Mean', 'Tackles-Mid 3rd Mean', 'Tackles-Att 3rd Mean', 
    'Challenges-Tkl Mean', 'Challenges-Att Mean', 'Challenges-Tkl% Mean', 
    'Challenges-Lost Mean', 'Blocks-Blocks Mean', 'Blocks-Sh Mean', 
    'Blocks-Pass Mean', 'Int Mean', 'Tkl+Int Mean', 'Clr Mean', 
    'Touches-Touches Mean', 'Touches-Def Pen Mean', 'Touches-Def 3rd Mean', 
    'Touches-Mid 3rd Mean', 'Touches-Att 3rd Mean', 'Touches-Att Pen Mean', 
    'Touches-Live Mean', 'Take-Ons-Att Mean', 'Take-Ons-Succ Mean', 
    'Take-Ons-Succ% Mean', 'Take-Ons-Tkld Mean', 'Take-Ons-Tkld% Mean', 
    'Carries-Carries Mean', 'Carries-TotDist Mean', 'Carries-PrgDist Mean', 
    'Carries-PrgC Mean', 'Carries-1/3 Mean', 'Carries-CPA Mean', 
    'Carries-Mis Mean', 'Carries-Dis Mean', 'Receiving-Rec Mean', 
    'Receiving-PrgR Mean', 'Playing Time-Mn/MP Mean', 'Playing Time-Min% Mean', 
    'Starts-Starts Mean', 'Starts-Mn/Start Mean', 'Starts-Compl Mean', 
    'Subs-Subs Mean', 'Subs-Mn/Sub Mean', 'Subs-unSub Mean', 
    'Team Success-PPM Mean', 'Team Success-onG Mean', 'Team Success-onGA Mean', 
    'Team Success-+/- Mean', 'Team Success-+/-90 Mean', 'Team Success-On-Off Mean', 
    'Team Success (xG)-onxG Mean', 'Team Success (xG)-onxGA Mean', 
    'Team Success (xG)-xG+/- Mean', 'Team Success (xG)-xG+/-90 Mean', 
    'Team Success (xG)-On-Off Mean', 'Performance-PKwon Mean', 
    'Performance-OG Mean', 'Performance-Recov Mean', 'Aerial Duels-Won Mean', 
    'Aerial Duels-Lost Mean', 'Aerial Duels-Won% Mean'
]

# List of statistics where lower is better
lower_is_better = [
    'Performance-CrdY Mean', 'Performance-CrdR Mean', 'Performance-2CrdY Mean', 
    'Performance-Fls Mean', 'Performance-Fld Mean', 'Performance-Off Mean', 
    'Performance-Crs Mean', 'Performance-Int Mean', 'Performance-TklW Mean', 
    'Performance-PKcon Mean', 'Err Mean'
]


# Normalize the statistics using min-max normalization
normalized_df = final_stats_df.copy()

# Normalize higher is better stats to a range of [0, 1]
for stat in higher_is_better:
    normalized_df[stat] = (normalized_df[stat] - normalized_df[stat].min()) / (normalized_df[stat].max() - normalized_df[stat].min())

# Normalize lower is better stats to a range of [0, 1] (inverted)
for stat in lower_is_better:
    normalized_df[stat] = 1 - ((normalized_df[stat] - normalized_df[stat].min()) / (normalized_df[stat].max() - normalized_df[stat].min()))

# Initialize a total score for each team
final_stats_df['Total_Score'] = 0

# Calculate the total score for each team
for stat in higher_is_better:
    final_stats_df['Total_Score'] += normalized_df[stat]

for stat in lower_is_better:
    final_stats_df['Total_Score'] += normalized_df[stat]

# Sort teams by total score from high to low
sorted_teams_df = final_stats_df.sort_values(by='Total_Score', ascending=False)

# Save the updated DataFrame with total scores to a CSV
sorted_teams_df.to_csv('./data/teams_with_scores.csv', index=True)

# Print the sorted teams and their total scores
print("Teams sorted by total score (high to low):")
print(sorted_teams_df[['Team', 'Total_Score']])

# Find the team with the highest total score
best_team = sorted_teams_df.loc[sorted_teams_df['Total_Score'].idxmax(), 'Team']
highest_total_score = sorted_teams_df['Total_Score'].max()

# Print the best overall team
print(f"\nThe best overall team based on the total score is: {best_team} with a score of {highest_total_score}")
