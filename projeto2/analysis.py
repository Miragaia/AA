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
    
    Accuracy is calculated as:
    - 100 * (exhaustive_weight / dynamic_weight)
    - 100 * (exhaustive_weight / greedy_weight)
    """

    base_dir = f"graphics/accuracy/{algorithm_type}"
    os.makedirs(base_dir, exist_ok=True)

    dynamic_merged = pd.merge(
        exhaustive_df, 
        dynamic_df, 
        on=["vertices_num", "percentage_max_num_edges"], 
        suffixes=('_exhaustive', '_dynamic')
    )
    greedy_merged = pd.merge(
        exhaustive_df, 
        greedy_df, 
        on=["vertices_num", "percentage_max_num_edges"], 
        suffixes=('_exhaustive', '_greedy')
    )

    dynamic_merged[f'{algorithm_type}_accuracy'] = (
        100 * (dynamic_merged['total_weight_exhaustive'] / dynamic_merged['total_weight_dynamic'])
    )
    greedy_merged['greedy_accuracy'] = (
        100 * (greedy_merged['total_weight_exhaustive'] / greedy_merged['total_weight_greedy'])
    )

    unique_densities = exhaustive_df['percentage_max_num_edges'].unique()

    for density in unique_densities:
        plt.figure(figsize=(10, 6))
        
        dynamic_subset = dynamic_merged[dynamic_merged['percentage_max_num_edges'] == density]
        greedy_subset = greedy_merged[greedy_merged['percentage_max_num_edges'] == density]

        if 'base_threshold' in dynamic_subset.columns and 'refine_threshold' in dynamic_subset.columns:
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
            plt.plot(
                dynamic_subset['vertices_num'], 
                dynamic_subset[f'{algorithm_type}_accuracy'], 
                marker='o', 
                label=f'{algorithm_type.capitalize()}'
            )

        plt.plot(
            greedy_subset['vertices_num'], 
            greedy_subset['greedy_accuracy'], 
            marker='s', 
            linestyle='--', 
            color='orange', 
            label='Greedy Algorithm'
        )
        
        plt.ylim(0, 105)
        plt.xlabel('Number of Vertices')
        plt.ylabel('Accuracy (%)')
        plt.title(f'Algorithm Accuracy Compared to Exhaustive Search (Density {int(density * 100)}%)')
        plt.legend()
        plt.grid(True)

        filename = f"{base_dir}/accuracy_density_{int(density * 100)}.png"
        plt.savefig(filename)
        plt.close()

    
def plot_weight_comparison_for_density_50(exhaustive_df, dynamic_df, greedy_df, algorithm_type):
    """
    Creates a bar plot comparing the weights of the set for exhaustive, greedy, 
    and all configurations of the specified algorithm type for a specific edge density of 50%.
    """

    density = 0.5
    base_dir = f"graphics/weight"
    os.makedirs(base_dir, exist_ok=True)

    exhaustive_subset = exhaustive_df[exhaustive_df['percentage_max_num_edges'] == density]
    dynamic_subset = dynamic_df[dynamic_df['percentage_max_num_edges'] == density]
    greedy_subset = greedy_df[greedy_df['percentage_max_num_edges'] == density]

    vertices = sorted(exhaustive_subset['vertices_num'].unique())
    bar_width = 0.2  
    x_positions = np.arange(len(vertices)) 

    exhaustive_weights = exhaustive_subset.set_index('vertices_num')['total_weight']
    plt.bar(x_positions, exhaustive_weights, bar_width, label='Exhaustive', color='blue')

    greedy_weights = greedy_subset.set_index('vertices_num')['total_weight']
    plt.bar(x_positions + bar_width, greedy_weights, bar_width, label='Greedy', color='orange')

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

    plt.xlabel('Number of Vertices')
    plt.ylabel('Total Weight')
    plt.title(f'Weight Comparison for Density 50% ({algorithm_type.capitalize()})')
    plt.xticks(x_positions + bar_width, vertices)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    filename = f"{base_dir}/weight_comparison_density_50_{algorithm_type}.png"
    plt.savefig(filename)
    plt.clf()


def plot_solution_size_bar_chart(data, algorithm_type):
    """
    Plots a bar chart of the occurrences of `solution_size` from the provided DataFrame.
    
    Parameters:
        data (pd.DataFrame): The dataset containing the `solution_size` column.
        algorithm_type (str): The type of algorithm (e.g., 'dynamic', 'randomized', 'dynamic_combined') 
                              to determine the save path and chart title.
    """

    save_dir = f"graphics/solution_size"
    os.makedirs(save_dir, exist_ok=True)

    if 'solution_size' not in data.columns:
        print("The column 'solution_size' is not present in the dataset.")
        return

    frequency_counts = data['solution_size'].value_counts().sort_index()

    plt.figure(figsize=(8, 6))
    plt.bar(frequency_counts.index, frequency_counts.values, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title(f'Bar Chart of Solution Size Occurrences ({algorithm_type.capitalize()})', fontsize=14)
    plt.xlabel('Solution Size', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(axis='y', alpha=0.75)
    plt.xticks(frequency_counts.index)
    plt.tight_layout()

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

    save_dir = f"graphics/execution_times"
    os.makedirs(save_dir, exist_ok=True)

    required_columns = {'execution_time', 'vertices_num', 'percentage_max_num_edges'}
    if not required_columns.issubset(data.columns):
        print(f"The dataset must contain the columns: {required_columns}")
        return

    grouped_data = data.groupby(['percentage_max_num_edges', 'vertices_num'])['execution_time'].mean().reset_index()

    unique_densities = grouped_data['percentage_max_num_edges'].unique()

    plt.figure(figsize=(10, 6))
    for density in sorted(unique_densities):
        subset = grouped_data[grouped_data['percentage_max_num_edges'] == density]
        plt.plot(
            subset['vertices_num'],
            subset['execution_time'],
            marker='o',
            label=f"Density {int(density * 100)}%"
        )
    

    plt.ylim(0)
    plt.title(f'Execution Time by Number of Vertices ({algorithm_type.capitalize()})', fontsize=14)
    plt.xlabel('Number of Vertices', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.legend(title="Edge Densities")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(sorted(data['vertices_num'].unique()), rotation=45)
    plt.tight_layout()

    filename = f"{save_dir}/execution_times_{algorithm_type}.png"
    plt.savefig(filename)
    plt.clf()
    

def plot_basic_operations(data, algorithm_type):
    """
    Plots a line chart of basic operations grouped by edge densities.

    Parameters:
        data (pd.DataFrame): The dataset containing `basic_operations`, `vertices_num`, and `percentage_max_num_edges`.
        algorithm_type (str): The type of algorithm (e.g., 'dynamic', 'randomized', 'dynamic_combined') to determine
                              the save path and chart title.
    """

    save_dir = f"graphics/basic_operations"
    os.makedirs(save_dir, exist_ok=True)

    required_columns = {'num_operations', 'vertices_num', 'percentage_max_num_edges'}
    if not required_columns.issubset(data.columns):
        print(f"The dataset must contain the columns: {required_columns}")
        return

    grouped_data = data.groupby(['percentage_max_num_edges', 'vertices_num'])['num_operations'].mean().reset_index()

    unique_densities = grouped_data['percentage_max_num_edges'].unique()

    plt.figure(figsize=(10, 6))
    for density in sorted(unique_densities):
        subset = grouped_data[grouped_data['percentage_max_num_edges'] == density]
        plt.plot(
            subset['vertices_num'],
            subset['num_operations'],
            marker='o',
            label=f"Density {int(density * 100)}%"
        )

    plt.yscale('log')
    plt.title(f'Basic Operations by Number of Vertices ({algorithm_type.capitalize()})', fontsize=14)
    plt.xlabel('Number of Vertices', fontsize=12)
    plt.ylabel('Basic Operations', fontsize=12)
    plt.legend(title="Edge Densities")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(sorted(data['vertices_num'].unique()), rotation=45)
    plt.tight_layout()

    filename = f"{save_dir}/basic_operations_{algorithm_type}.png"
    plt.savefig(filename)
    plt.clf()
    plt.close()

def plot_weight_comparison(dynamic_combined_df, dynamic_df):
    """
    Creates line charts comparing the weights of the dynamic combined and dynamic algorithms, 
    with one chart per density. The plot extends to the maximum number of vertices.

    Parameters:
        dynamic_combined_df (pd.DataFrame): DataFrame for the dynamic combined algorithm.
        dynamic_df (pd.DataFrame): DataFrame for the dynamic algorithm.
    """

    save_dir = f"graphics/weight_comparison"
    os.makedirs(save_dir, exist_ok=True)

    dynamic_combined_df = (
        dynamic_combined_df.groupby(['vertices_num', 'percentage_max_num_edges'])
        .mean()
        .reset_index()
        .rename(columns={'total_weight': 'dynamic_combined_weight'})
    )
    dynamic_df = (
        dynamic_df.groupby(['vertices_num', 'percentage_max_num_edges'])
        .mean()
        .reset_index()
        .rename(columns={'total_weight': 'dynamic_weight'})
    )

    merged_data = pd.merge(dynamic_combined_df, dynamic_df, on=['vertices_num', 'percentage_max_num_edges'])

    unique_densities = merged_data['percentage_max_num_edges'].unique()

    for density in sorted(unique_densities):
        plt.figure(figsize=(10, 6))

        subset = merged_data[merged_data['percentage_max_num_edges'] == density]

        plt.plot(
            subset['vertices_num'],
            subset['dynamic_combined_weight'],
            marker='o',
            label="Dynamic Combined",
        )
        plt.plot(
            subset['vertices_num'],
            subset['dynamic_weight'],
            marker='s',
            linestyle='--',
            label="Dynamic",
        )

        plt.title(f'Weight Comparison of Algorithms (Density {int(density * 100)}%)', fontsize=14)
        plt.xlabel('Number of Vertices', fontsize=12)
        plt.ylabel('Total Weight (Lower is Better)', fontsize=12)
        plt.legend(title="Algorithms")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(sorted(subset['vertices_num'].unique()), rotation=45)
        plt.tight_layout()

        filename = f"{save_dir}/weight_comparison_density_{int(density * 100)}.png"
        plt.savefig(filename)
        plt.clf()
        plt.close()
