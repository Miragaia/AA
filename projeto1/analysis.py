import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def save_to_csv(df, filename):
    df.to_csv(f"results/{filename}", index=False)
    print(f"Results saved to {filename}")

def executions_times(df, algorithm_name):
    unique_densities = df['percentage_max_num_edges'].unique()
    for density in unique_densities:
        subset = df[df['percentage_max_num_edges'] == density]
        plt.plot(subset['vertices_num'], subset['execution_time'], marker='o', label=f"{algorithm_name} - {int(density * 100)}%")
    
    plt.xlabel("Number of Vertices")
    plt.ylabel("Execution Time (s)")
    plt.title(f"Execution Time - {algorithm_name}")
    plt.legend()
    plt.savefig(f"graphics/executions_times/{algorithm_name}_execution_times.png")
    plt.clf()

def basic_operations_num(df, algorithm_name):
    unique_densities = df['percentage_max_num_edges'].unique()
    plt.figure(figsize=(10, 6))

    for density in unique_densities:
        subset = df[df['percentage_max_num_edges'] == density]
        plt.plot(subset['vertices_num'], subset['num_operations'], marker='o', linestyle='-', label=f"{int(density * 100)}% Density")
    
    plt.xlabel('Number of Vertices')
    plt.ylabel('Number of Basic Operations')
    plt.title(f'Basic Operations Count for {algorithm_name}')
    plt.yscale('log')
    plt.legend()
    plt.savefig(f"graphics/basic_ops/{algorithm_name}_basic_ops.png")
    plt.clf()

def basic_operations_num_aggregated(df_exhaustive, df_greedy):
    unique_densities_exhaustive = df_exhaustive['percentage_max_num_edges'].unique()
    unique_densities_greedy = df_greedy['percentage_max_num_edges'].unique()
    
    plt.figure(figsize=(10, 6))

    for density in unique_densities_exhaustive:
        subset = df_exhaustive[df_exhaustive['percentage_max_num_edges'] == density]
        plt.plot(
            subset['vertices_num'], 
            subset['num_operations'], 
            marker='o', 
            linestyle='-', 
            label=f"Exhaustive - {int(density * 100)}% Density"
        )

    for density in unique_densities_greedy:
        subset = df_greedy[df_greedy['percentage_max_num_edges'] == density]
        plt.plot(
            subset['vertices_num'], 
            subset['num_operations'], 
            marker='x', 
            linestyle='--', 
            label=f"Greedy - {int(density * 100)}% Density"
        )
    
    plt.xlabel('Number of Vertices')
    plt.ylabel('Number of Basic Operations')
    plt.title('Basic Operations Count for Exhaustive Search and Greedy Heuristic')
    plt.yscale('log')
    plt.legend()
    plt.savefig("graphics/basic_ops/combined_basic_ops.png")
    plt.clf()

def plot_time_complexity(df_exhaustive, df_greedy):
    plt.figure(figsize=(10, 6))

    for density in df_exhaustive['percentage_max_num_edges'].unique():
        subset_exhaustive = df_exhaustive[df_exhaustive['percentage_max_num_edges'] == density]
        subset_greedy = df_greedy[df_greedy['percentage_max_num_edges'] == density]

        plt.plot(subset_exhaustive['vertices_num'], subset_exhaustive['execution_time'], label=f'Exhaustive - {int(density * 100)}% Density', marker='o')
        plt.plot(subset_greedy['vertices_num'], subset_greedy['execution_time'], label=f'Greedy - {int(density * 100)}% Density', marker='x')

    plt.xlabel('Number of Vertices')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Time Complexity by Number of Vertices')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.savefig("graphics/time_complexity/time_complexity_plot.png")
    plt.clf()

def compare_solutions(comparison_df):
    unique_percentages = comparison_df['percentage_max_num_edges'].unique()
    
    for percentage in unique_percentages:
        subset = comparison_df[comparison_df['percentage_max_num_edges'] == percentage]

        plt.plot(subset['vertices_num'], subset['exhaustive_total_weight'], marker='+', color='red', label='Exhaustive Search')
        plt.plot(subset['vertices_num'], subset['greedy_total_weight'], marker='x', color='blue', label='Greedy Heuristic')
        plt.title(f"Total Weight Comparison - {int(percentage * 100)}% Edge Density")
        plt.xlabel("Number of Vertices")
        plt.ylabel("Total Weight")
        plt.legend()
        plt.savefig(f"graphics/weights/total_weight_comparison_{int(percentage * 100)}.png")
        plt.clf()

        plt.plot(subset['vertices_num'], subset['time_ratio'], marker='o', color='purple')
        plt.title(f"Execution Time Ratio (Greedy / Exhaustive) - {int(percentage * 100)}% Edge Density")
        plt.xlabel("Number of Vertices")
        plt.ylabel("Time Ratio (Greedy / Exhaustive)")
        plt.savefig(f"graphics/time_ratio/execution_time_ratio_{int(percentage * 100)}.png")
        plt.clf()

def predict_large_graph_times_75(df_exhaustive, df_greedy, vertices_to_predict):
    # Filter data for 75% edge density
    df_exhaustive_75 = df_exhaustive[df_exhaustive['percentage_max_num_edges'] == 0.75]
    df_greedy_75 = df_greedy[df_greedy['percentage_max_num_edges'] == 0.75]
    
    # Use the known point (10 vertices, 75% density, 698.9304 seconds) for the exhaustive search coefficient
    vertices_exhaustive_8 = 8
    time_exhaustive_8 = 698.9304
    coef_exhaustive = time_exhaustive_8 / (2 ** vertices_exhaustive_8)

    # Calculate coefficient for greedy approach as before
    vertices_greedy = df_greedy_75['vertices_num'].to_numpy()
    time_greedy = df_greedy_75['execution_time'].to_numpy()
    edges_greedy = vertices_greedy * (vertices_greedy - 1) // 2
    coef_greedy = np.mean(time_greedy / (edges_greedy * np.log2(edges_greedy + 1)))

    # Create predictions for new vertex sizes
    predicted_times_exhaustive = []
    predicted_times_greedy = []

    for vertices in vertices_to_predict:
        edges = vertices * (vertices - 1) // 2
        time_exhaustive_pred = coef_exhaustive * (2 ** vertices)
        time_greedy_pred = coef_greedy * (edges * np.log2(edges + 1))
        
        predicted_times_exhaustive.append((vertices, time_exhaustive_pred))
        predicted_times_greedy.append((vertices, time_greedy_pred))

    # Create DataFrames for saving results
    df_pred_exhaustive = pd.DataFrame(predicted_times_exhaustive, columns=['vertices_num', 'predicted_execution_time'])
    df_pred_greedy = pd.DataFrame(predicted_times_greedy, columns=['vertices_num', 'predicted_execution_time'])

    # Save predictions to CSV
    save_to_csv(df_pred_exhaustive, 'predicted_times_exhaustive_75.csv')
    save_to_csv(df_pred_greedy, 'predicted_times_greedy_75.csv')

    # Plotting predictions along with original data
    plt.figure(figsize=(10, 6))

    # Plot original data
    plt.plot(df_exhaustive_75['vertices_num'], df_exhaustive_75['execution_time'], 'o-', label="Exhaustive - Actual", color='red')
    plt.plot(df_greedy_75['vertices_num'], df_greedy_75['execution_time'], 'x-', label="Greedy - Actual", color='blue')

    # Plot predictions for larger graphs
    plt.plot(df_pred_exhaustive['vertices_num'], df_pred_exhaustive['predicted_execution_time'], 'o--', label="Exhaustive - Predicted", color='darkred')
    plt.plot(df_pred_greedy['vertices_num'], df_pred_greedy['predicted_execution_time'], 'x--', label="Greedy - Predicted", color='darkblue')

    # Formatting the plot
    plt.xlabel("Number of Vertices")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Predicted Time Complexity for Larger Graphs (75% Edge Density)")
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.savefig("graphics/predicted_time_complexity/large_graph_predictions_75_density.png")
    plt.clf()

    print("Predicted execution times for 75% density plotted and saved.")

def predict_large_graph_space(vertices_to_predict, densities=[0.125, 0.25, 0.5, 0.75]):
    predicted_space_exhaustive = {}
    predicted_space_greedy = {}

    for density in densities:
        space_exhaustive_density = []
        space_greedy_density = []

        for vertices in vertices_to_predict:
            # Calculate edges based on density
            edges = int(vertices * (vertices - 1) * density / 2)

            # Space complexity for exhaustive (2^V)
            space_exhaustive = 2 ** vertices
            space_exhaustive_density.append(space_exhaustive)

            # Space complexity for greedy (V + E)
            space_greedy = vertices + edges
            space_greedy_density.append(space_greedy)

        # Store results for each density level
        predicted_space_exhaustive[density] = space_exhaustive_density
        predicted_space_greedy[density] = space_greedy_density

    # Visualization
    plt.figure(figsize=(12, 8))

    # Plot exhaustive predictions
    for density, space_data in predicted_space_exhaustive.items():
        plt.plot(vertices_to_predict, space_data, label=f"Exhaustive - {int(density * 100)}% Density", linestyle='--', marker='o')

    # Plot greedy predictions
    for density, space_data in predicted_space_greedy.items():
        plt.plot(vertices_to_predict, space_data, label=f"Greedy - {int(density * 100)}% Density", linestyle='-', marker='x')

    # Formatting the plot
    plt.xlabel("Number of Vertices")
    plt.ylabel("Space Complexity (Units)")
    plt.yscale('log')
    plt.title("Predicted Space Complexity for Various Densities")
    plt.legend()
    plt.grid(True)
    plt.savefig("graphics/predicted_space_complexity/space_complexity_predictions.png")
    plt.clf()

    print("Predicted space complexities plotted and saved.")
