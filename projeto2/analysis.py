import pandas as pd
import matplotlib.pyplot as plt
import os

def save_to_csv(df, filename):
    df.to_csv(f"results/{filename}", index=False)
    print(f"Results saved to {filename}")

def save_to_csv_dynamic(df, filename):
    df.to_csv(f"results/dynamic/{filename}", index=False)
    print(f"Results saved to {filename}")

def load_exhaustive_results():
    """Load the exhaustive search results from CSV."""
    return pd.read_csv("results/exhaustive_results.csv")

def load_dynamic_results():
    """Load dynamic results from the specified folder."""
    dynamic_results = []
    for file_name in os.listdir("results/dynamic/"):
        if file_name.endswith(".csv"):
            file_path = os.path.join("results/dynamic/", file_name)
            dynamic_results.append(pd.read_csv(file_path))
    return pd.concat(dynamic_results, ignore_index=True)

def plot_accuracy(exhaustive_df, dynamic_df):
    """
    Plots the accuracy of dynamic results compared to exhaustive results as separate line charts for different edge densities.
    Accuracy is calculated as:
    Accuracy = 100 * (1 - abs(Dynamic Total Weight - Exhaustive Total Weight) / Exhaustive Total Weight)
    """
    # Merge the dynamic and exhaustive results to calculate accuracy
    merged_df = pd.merge(exhaustive_df, dynamic_df, on=["vertices_num", "percentage_max_num_edges"], suffixes=('_exhaustive', '_dynamic'))
    
    # Calculate accuracy for each entry
    merged_df['accuracy'] = 100 * (1 - abs(merged_df['total_weight_dynamic'] - merged_df['total_weight_exhaustive']) / merged_df['total_weight_exhaustive'])
    
    # Get unique edge densities
    unique_densities = merged_df['percentage_max_num_edges'].unique()

    # Loop through each edge density and plot accuracy separately
    for density in unique_densities:
        plt.figure(figsize=(10, 6))
        # Filter data based on current edge density
        subset = merged_df[merged_df['percentage_max_num_edges'] == density]
        
        # Get unique threshold pairs for the current density
        threshold_pairs = subset[['base_threshold', 'refine_threshold']].drop_duplicates()

        # Plot accuracy for each threshold pair at this density
        for _, thresholds in threshold_pairs.iterrows():
            base_threshold = thresholds['base_threshold']
            refine_threshold = thresholds['refine_threshold']

            # Filter data for this threshold pair
            threshold_subset = subset[(subset['base_threshold'] == base_threshold) & (subset['refine_threshold'] == refine_threshold)]

            # Plot accuracy vs vertices number for this threshold combination
            plt.plot(threshold_subset['vertices_num'], threshold_subset['accuracy'], marker='o', label=f'Base {base_threshold}, Refine {refine_threshold}')
        
        # Customize plot labels and title
        plt.xlabel('Number of Vertices')
        plt.ylabel('Accuracy (%)')
        plt.title(f'Dynamic Algorithm Accuracy Compared to Exhaustive Search (Density {int(density * 100)}%)')
        plt.legend()
        plt.grid(True)

        # Save the plot to a separate file for this density
        plt.savefig(f"graphics/accuracy/dynamic_accuracy_density_{int(density * 100)}.png")
        plt.clf()
