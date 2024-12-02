import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def save_to_csv(df, filename):
    df.to_csv(f"results/{filename}", index=False)
    print(f"Results saved to {filename}")

def save_to_csv_dynamic_randomized(df, filename):
    df.to_csv(f"results/dynamic/randomized/{filename}", index=False)
    print(f"Results saved to {filename}")

def save_to_csv_dynamic_combined(df, filename):
    df.to_csv(f"results/dynamic/combined/{filename}", index=False)
    print(f"Results saved to {filename}")

def load_exhaustive_results():
    """Load the exhaustive search results from CSV."""
    return pd.read_csv("results/exhaustive_results.csv")

def load_dynamic_results():
    """Load dynamic results from the specified folder."""
    dynamic_results = []
    for file_name in os.listdir("results/dynamic/randomized"):
        if file_name.endswith(".csv"):
            file_path = os.path.join("results/dynamic/randomized", file_name)
            dynamic_results.append(pd.read_csv(file_path))
    return pd.concat(dynamic_results, ignore_index=True)

def load_dynamic_combined_results():
    """Load dynamic results from the specified folder."""
    dynamic_results = []
    for file_name in os.listdir("results/dynamic/combined"):
        if file_name.endswith(".csv"):
            file_path = os.path.join("results/dynamic/combined", file_name)
            dynamic_results.append(pd.read_csv(file_path))
    return pd.concat(dynamic_results, ignore_index=True)

def plot_accuracy(exhaustive_df, dynamic_df, greedy_df, algorithm_type):
    """
    Plots the accuracy of dynamic and greedy algorithms compared to exhaustive results as separate line charts for different edge densities.
    Saves results into different directories based on the algorithm type.
    """
    import os

    # Determine directory based on algorithm type
    base_dir = f"graphics/accuracy/{algorithm_type}"
    os.makedirs(base_dir, exist_ok=True)

    # Merge the exhaustive and dynamic/randomized results
    dynamic_merged = pd.merge(exhaustive_df, dynamic_df, on=["vertices_num", "percentage_max_num_edges"], suffixes=('_exhaustive', '_dynamic'))
    greedy_merged = pd.merge(exhaustive_df, greedy_df, on=["vertices_num", "percentage_max_num_edges"], suffixes=('_exhaustive', '_greedy'))

    # Calculate accuracy for dynamic/randomized and greedy
    dynamic_merged[f'{algorithm_type}_accuracy'] = 100 * (
        1 - abs(dynamic_merged[f'total_weight_dynamic'] - dynamic_merged['total_weight_exhaustive']) / dynamic_merged['total_weight_exhaustive']
    )
    greedy_merged['greedy_accuracy'] = 100 * (
        1 - abs(greedy_merged['total_weight_greedy'] - greedy_merged['total_weight_exhaustive']) / greedy_merged['total_weight_exhaustive']
    )

    # Get unique edge densities
    unique_densities = exhaustive_df['percentage_max_num_edges'].unique()

    # Loop through each edge density and plot accuracy separately
    for density in unique_densities:
        plt.figure(figsize=(10, 6))
        
        # Filter data based on current edge density
        dynamic_subset = dynamic_merged[dynamic_merged['percentage_max_num_edges'] == density]
        greedy_subset = greedy_merged[greedy_merged['percentage_max_num_edges'] == density]

        # Check if base_threshold and refine_threshold exist in the dataset
        if 'base_threshold' in dynamic_subset.columns and 'refine_threshold' in dynamic_subset.columns:
            # Plot dynamic/randomized accuracy for each threshold pair
            threshold_pairs = dynamic_subset[['base_threshold', 'refine_threshold']].drop_duplicates()
            for _, thresholds in threshold_pairs.iterrows():
                base_threshold = thresholds['base_threshold']
                refine_threshold = thresholds['refine_threshold']
                threshold_subset = dynamic_subset[
                    (dynamic_subset['base_threshold'] == base_threshold) & 
                    (dynamic_subset['refine_threshold'] == refine_threshold)
                ]
                plt.plot(
                    threshold_subset['vertices_num'], 
                    threshold_subset[f'{algorithm_type}_accuracy'], 
                    marker='o', 
                    label=f'{algorithm_type.capitalize()}: Base {base_threshold}, Refine {refine_threshold}'
                )
        else:
            # If thresholds are not present, plot only the overall accuracy
            plt.plot(
                dynamic_subset['vertices_num'], 
                dynamic_subset[f'{algorithm_type}_accuracy'], 
                marker='o', 
                label=f'{algorithm_type.capitalize()}'
            )

        # Plot greedy accuracy as a single line
        plt.plot(
            greedy_subset['vertices_num'], 
            greedy_subset['greedy_accuracy'], 
            marker='s', 
            linestyle='--', 
            color='orange', 
            label='Greedy Algorithm'
        )
        
        # Customize plot labels and title
        plt.xlabel('Number of Vertices')
        plt.ylabel('Accuracy (%)')
        plt.title(f'Algorithm Accuracy Compared to Exhaustive Search (Density {int(density * 100)}%)')
        plt.legend()
        plt.grid(True)

        # Save the plot to a directory for the specified algorithm type
        filename = f"{base_dir}/accuracy_density_{int(density * 100)}.png"
        plt.savefig(filename)
        plt.clf()


    
def plot_weight_comparison_for_density_50(exhaustive_df, dynamic_df, greedy_df, algorithm_type):
    """
    Creates a bar plot comparing the weights of the set for exhaustive, greedy, 
    and all configurations of the specified algorithm type for a specific edge density of 50%.
    Saves the plot to a directory based on the algorithm type.
    """
    import os

    # Define density and create directory for saving results
    density = 0.5
    base_dir = f"graphics/weight"
    os.makedirs(base_dir, exist_ok=True)

    # Filter data for 50% density
    exhaustive_subset = exhaustive_df[exhaustive_df['percentage_max_num_edges'] == density]
    dynamic_subset = dynamic_df[dynamic_df['percentage_max_num_edges'] == density]
    greedy_subset = greedy_df[greedy_df['percentage_max_num_edges'] == density]

    # Prepare data for plotting
    vertices = sorted(exhaustive_subset['vertices_num'].unique())
    bar_width = 0.2  # Width of each bar
    x_positions = np.arange(len(vertices))  # Base positions for bars

    # Plot exhaustive weights
    exhaustive_weights = exhaustive_subset.set_index('vertices_num')['total_weight']
    plt.bar(x_positions, exhaustive_weights, bar_width, label='Exhaustive', color='blue')

    # Plot greedy weights
    greedy_weights = greedy_subset.set_index('vertices_num')['total_weight']
    plt.bar(x_positions + bar_width, greedy_weights, bar_width, label='Greedy', color='orange')

    # Plot weights for the selected algorithm type (average for each configuration)
    dynamic_weights = []
    for v in vertices:
        dynamic_for_vertex = dynamic_subset[dynamic_subset['vertices_num'] == v]
        dynamic_weights.append(dynamic_for_vertex['total_weight'].mean())
    plt.bar(
        x_positions + 2 * bar_width, 
        dynamic_weights, 
        bar_width, 
        label=f'{algorithm_type.capitalize()} (Avg)', 
        color='green'
    )

    # Customize the plot
    plt.xlabel('Number of Vertices')
    plt.ylabel('Total Weight')
    plt.title(f'Weight Comparison for Density 50% ({algorithm_type.capitalize()})')
    plt.xticks(x_positions + bar_width, vertices)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the plot
    plt.tight_layout()
    filename = f"{base_dir}/weight_comparison_density_50_{algorithm_type}.png"
    plt.savefig(filename)
    plt.clf()

def plot_solution_size_bar_chart(data, algorithm_type):
    """
    Plots a bar chart of the occurrences of `solution_size` from the provided DataFrame.
    
    The results are saved dynamically based on the specified algorithm type.
    
    Parameters:
        data (pd.DataFrame): The dataset containing the `solution_size` column.
        algorithm_type (str): The type of algorithm (e.g., 'dynamic', 'randomized', 'dynamic_combined') 
                              to determine the save path and chart title.
    """

    # Define save directory based on algorithm type
    save_dir = f"graphics/solution_size"
    os.makedirs(save_dir, exist_ok=True)

    # Check if 'solution_size' column exists
    if 'solution_size' not in data.columns:
        print("The column 'solution_size' is not present in the dataset.")
        return

    # Calculate frequencies of solution_size values
    frequency_counts = data['solution_size'].value_counts().sort_index()

    # Plot the bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(frequency_counts.index, frequency_counts.values, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title(f'Bar Chart of Solution Size Occurrences ({algorithm_type.capitalize()})', fontsize=14)
    plt.xlabel('Solution Size', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(axis='y', alpha=0.75)
    plt.xticks(frequency_counts.index)
    plt.tight_layout()

    # Save the plot
    filename = f"{save_dir}/solution_size_bar_chart_{algorithm_type}.png"
    plt.savefig(filename)
    plt.clf()

def plot_execution_times(data, algorithm_type):
    """
    Plots a line chart of execution times grouped by edge densities.

    Parameters:
        data (pd.DataFrame): The dataset containing `execution_time`, `vertices_num`, and `percentage_max_num_edges`.
        algorithm_type (str): The type of algorithm (e.g., 'dynamic', 'randomized', 'dynamic_combined') to determine
                              the save path and chart title.
    """
    import os

    # Define save directory based on algorithm type
    save_dir = f"graphics/execution_times"
    os.makedirs(save_dir, exist_ok=True)

    # Check if required columns exist
    required_columns = {'execution_time', 'vertices_num', 'percentage_max_num_edges'}
    if not required_columns.issubset(data.columns):
        print(f"The dataset must contain the columns: {required_columns}")
        return

    # Group data by edge density and vertices, then calculate mean execution times
    grouped_data = data.groupby(['percentage_max_num_edges', 'vertices_num'])['execution_time'].mean().reset_index()

    # Get unique edge densities
    unique_densities = grouped_data['percentage_max_num_edges'].unique()

    # Plot the execution times for each edge density
    plt.figure(figsize=(10, 6))
    for density in sorted(unique_densities):
        subset = grouped_data[grouped_data['percentage_max_num_edges'] == density]
        plt.plot(
            subset['vertices_num'],
            subset['execution_time'],
            marker='o',
            label=f"Density {int(density * 100)}%"
        )

    # Customize the plot
    plt.title(f'Execution Time by Number of Vertices ({algorithm_type.capitalize()})', fontsize=14)
    plt.xlabel('Number of Vertices', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.legend(title="Edge Densities")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(sorted(data['vertices_num'].unique()), rotation=45)
    plt.tight_layout()

    # Save the plot
    filename = f"{save_dir}/execution_times_{algorithm_type}.png"
    plt.savefig(filename)
    plt.clf()



