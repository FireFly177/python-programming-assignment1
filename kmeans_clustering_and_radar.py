import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
import matplotlib.pyplot as plt
from math import pi

# Step 1: Load data and preprocessing
def load_data(file_path):
    df = pd.read_csv(file_path)
    
    df.replace('N/a', np.nan, inplace=True)

    exclude_cols = ['Player', 'Nation', 'Pos', 'Squad']
    
    # Convert object columns to numeric, excluding the non-statistical ones
    for col in df.columns:
        if df[col].dtype == 'object' and col not in exclude_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Get numeric columns after conversion
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    return df, numeric_cols

def perform_kmeans(df, stats_cols, important_cols):
    # Drop rows with NaNs in important columns for clustering
    df_filtered = df.dropna(subset=important_cols)

    # Scale the important columns
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_filtered[important_cols])  # Use important_cols for scaling

    # Determine the optimal number of clusters using the elbow method
    inertia = []
    for k in range(1, 11):  # Test cluster sizes from 1 to 10
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(df_scaled)
        inertia.append(kmeans.inertia_)

    # Plotting the elbow method (optional, can be placed elsewhere)
    plt.figure(figsize=(8, 4))
    plt.plot(range(1, 11), inertia, marker='o')
    plt.title('Elbow Method for Optimal k')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.grid(True)
    plt.show()

    # Fit KMeans with the optimal number of clusters (you might want to choose based on the elbow plot)
    optimal_k = 4  # Set this after analyzing the elbow plot
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    kmeans.fit(df_scaled)

    return df_scaled  # Return the scaled DataFrame for PCA



# Step 3: Apply PCA and Plot in 2D
def pca_and_plot(df_scaled, num_clusters):
    pca = PCA(n_components=2)
    df_pca = pca.fit_transform(df_scaled)

    # Apply K-means with optimal K
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(df_scaled)

    # Plot the PCA-transformed data with cluster labels
    plt.figure(figsize=(8, 6))
    plt.scatter(df_pca[:, 0], df_pca[:, 1], c=clusters, cmap='viridis')
    plt.title(f'K-means Clustering with {num_clusters} clusters (PCA reduced)')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.show()

# Step 4: Radar Chart to Compare Two Players
def radar_chart(df, player1, player2, attributes):
    # Extract data for the two players
    p1_data = df[df['Player'] == player1][attributes].values.flatten()
    p2_data = df[df['Player'] == player2][attributes].values.flatten()

    # Create radar chart
    categories = attributes
    num_vars = len(categories)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Close the plot

    p1_data = np.append(p1_data, p1_data[0])  # Close the plot
    p2_data = np.append(p2_data, p2_data[0])  # Close the plot

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.fill(angles, p1_data, color='blue', alpha=0.25)
    ax.fill(angles, p2_data, color='red', alpha=0.25)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    plt.title(f'{player1} (Blue) vs {player2} (Red) Radar Chart', size=15, color='black', y=1.1)
    plt.show()

# Step 5: Main function
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare two players using a radar chart.')
    parser.add_argument('--p1', type=str, required=True, help='First player name')
    parser.add_argument('--p2', type=str, required=True, help='Second player name')
    parser.add_argument('--Attribute', type=str, required=True, help='Comma-separated list of attributes to compare')
    args = parser.parse_args()

    player1 = args.p1
    player2 = args.p2
    attributes = args.Attribute.split(',')

    # Load data
    df, stats_cols = load_data('./data/merged_premier_league_stats.csv')

    # Specify the important columns for clustering
    important_cols = attributes  # Update this with your desired attributes

    # Drop rows with NaNs in important columns
    df.dropna(subset=important_cols, inplace=True)

    # Perform K-means clustering
    df_scaled = perform_kmeans(df, stats_cols, important_cols)

    # Use PCA and plot
    num_clusters = 4  # Adjust this based on elbow method results
    pca_and_plot(df_scaled, num_clusters)

    # Radar chart comparison
    radar_chart(df, player1, player2, attributes)

