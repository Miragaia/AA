import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RESULTS_DIR = "../data/results/"
GRAPHICS_DIR = "../data/graphics/"  # Directory to save the visualizations
CSV_FILE = "../data/performance_metrics.csv"  # Path to the CSV file

def load_results(folder):
    """
    Load all results from a folder.

    Args:
        folder (str): Directory containing JSON result files.

    Returns:
        dict: A dictionary of filename to results.
    """
    files = Path(folder).glob("*.json")
    results = {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            results[file.stem] = json.load(f)
    return results

def visualize_comparative_results():
    """
    Generate and save comparative visualizations of word frequencies between counters.
    """
    exact_results = load_results(RESULTS_DIR + "exact/")
    csuros_results = load_results(RESULTS_DIR + "csuros/")
    stream_results = load_results(RESULTS_DIR + "stream/")

    graphics_path = Path(GRAPHICS_DIR)
    graphics_path.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    for filename in exact_results:
        exact_data = exact_results[filename]
        csuros_data = csuros_results.get(filename, {})
        stream_data = stream_results.get(filename, {})

        # Get the top 10 words based on exact counts
        top_words = sorted(exact_data.items(), key=lambda x: x[1], reverse=True)[:10]
        words = [word for word, _ in top_words]

        # Gather counts for comparison
        exact_counts = [exact_data.get(word, 0) for word in words]
        csuros_counts = [csuros_data.get(word, 0) for word in words]
        stream_counts = [stream_data.get(word, 0) for word in words]

        # Create a comparative bar chart
        x = np.arange(len(words))
        width = 0.25  # Width of each bar

        plt.figure(figsize=(12, 7))
        plt.bar(x - width, exact_counts, width, label="Exact Counter", color="blue")
        plt.bar(x, csuros_counts, width, label="Csuros Counter", color="orange")
        plt.bar(x + width, stream_counts, width, label="Stream Counter", color="green")

        plt.title(f"Top 10 Words Frequency Comparison - {filename}")
        plt.xlabel("Words")
        plt.ylabel("Counts")
        plt.xticks(x, words, rotation=45)
        plt.legend()
        plt.tight_layout()

        # Save the plot
        output_file = graphics_path / f"{filename}_comparative_top10.png"
        plt.savefig(output_file)
        print(f"Comparative visualization saved to: {output_file}")

        plt.close()  # Close the plot to free memory

def visualize_performance_metrics():
    """
    Generate and save visualizations for execution time and memory usage.
    """
    # Load the performance CSV
    df = pd.read_csv(CSV_FILE)

    graphics_path = Path(GRAPHICS_DIR)
    graphics_path.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    # Plot Execution Time
    plt.figure(figsize=(10, 6))
    for algorithm in df['algorithm'].unique():
        subset = df[df['algorithm'] == algorithm]
        plt.plot(subset['filename'], subset['execution_time'], label=algorithm)

    plt.title("Execution Time Comparison")
    plt.xlabel("Filename")
    plt.ylabel("Execution Time (seconds)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    execution_time_file = graphics_path / "execution_time_comparison.png"
    plt.savefig(execution_time_file)
    print(f"Execution time comparison saved to: {execution_time_file}")
    plt.close()

    # Plot Memory Usage
    plt.figure(figsize=(10, 6))
    for algorithm in df['algorithm'].unique():
        subset = df[df['algorithm'] == algorithm]
        plt.plot(subset['filename'], subset['memory_usage'], label=algorithm)

    plt.title("Memory Usage Comparison")
    plt.xlabel("Filename")
    plt.ylabel("Memory Usage (KB)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    memory_usage_file = graphics_path / "memory_usage_comparison.png"
    plt.savefig(memory_usage_file)
    print(f"Memory usage comparison saved to: {memory_usage_file}")
    plt.close()

def compare_results():
    """
    Compare exact, approximate, and stream results.
    """
    exact_results = load_results(RESULTS_DIR + "exact/")
    csuros_results = load_results(RESULTS_DIR + "csuros/")
    stream_results = load_results(RESULTS_DIR + "stream/")

    # Example comparison: top words in exact vs. approximate vs. stream
    for filename in exact_results:
        print(f"\nComparing results for '{filename}':")
        exact_top = sorted(exact_results[filename].items(), key=lambda x: x[1], reverse=True)[:10]
        print("Exact Top 10:", exact_top)

        if filename in csuros_results:
            csuros_top = sorted(csuros_results[filename].items(), key=lambda x: x[1], reverse=True)[:10]
            print("Csuros Top 10:", csuros_top)

        if filename in stream_results:
            stream_top = sorted(stream_results[filename].items(), key=lambda x: x[1], reverse=True)[:10]
            print("Stream Top 10:", stream_top)

if __name__ == "__main__":
    compare_results()
    visualize_comparative_results()
    visualize_performance_metrics()
