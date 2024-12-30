import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

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


def calculate_errors(exact, approximate):
    """
    Calculate absolute and relative errors between exact and approximate results.

    Args:
        exact (dict): Exact word frequency results.
        approximate (dict): Approximate word frequency results.

    Returns:
        dict: A dictionary containing absolute and relative errors for each word.
    """
    errors = {}
    for word, exact_count in exact.items():
        approx_count = approximate.get(word, 0)
        absolute_error = abs(exact_count - approx_count)
        relative_error = absolute_error / exact_count if exact_count != 0 else 0
        errors[word] = {"absolute_error": absolute_error, "relative_error": relative_error}
    return errors


def summarize_errors(errors):
    """
    Summarize error statistics.

    Args:
        errors (dict): A dictionary of errors for each word.

    Returns:
        dict: A dictionary with summary statistics for absolute and relative errors.
    """
    absolute_errors = [v["absolute_error"] for v in errors.values()]
    relative_errors = [v["relative_error"] for v in errors.values()]

    summary = {
        "absolute_error": {
            "lowest": min(absolute_errors, default=0),
            "highest": max(absolute_errors, default=0),
            "average": np.mean(absolute_errors) if absolute_errors else 0,
            "total": sum(absolute_errors),
        },
        "relative_error": {
            "lowest": min(relative_errors, default=0),
            "highest": max(relative_errors, default=0),
            "average": np.mean(relative_errors) if relative_errors else 0,
            "total": sum(relative_errors),
        },
    }
    return summary


def save_all_summaries_to_csv(all_summaries, output_file):
    """
    Save all error summaries to a single CSV file.

    Args:
        all_summaries (list): List of summaries for all files.
        output_file (str): Path to save the CSV file.
    """
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow([
            "Filename", "Error Type", "Lowest Value", "Highest Value", "Average Value", "Total Value"
        ])

        # Write data
        for summary in all_summaries:
            filename = summary["filename"]
            for error_type, metrics in summary["errors"].items():
                writer.writerow([
                    filename,
                    error_type,
                    metrics["lowest"],
                    metrics["highest"],
                    metrics["average"],
                    metrics["total"],
                ])


def analyze_errors():
    """
    Perform error analysis and save all summaries to a single CSV file.
    """
    exact_results = load_results(RESULTS_DIR + "exact/")
    csuros_results = load_results(RESULTS_DIR + "csuros/")
    stream_results = load_results(RESULTS_DIR + "stream/")

    all_summaries = []

    for filename in exact_results:
        exact_data = exact_results[filename]
        csuros_data = csuros_results.get(filename, {})
        stream_data = stream_results.get(filename, {})

        print(f"\nAnalyzing errors for '{filename}'...")

        # Calculate errors and summaries for Csuros
        csuros_errors = calculate_errors(exact_data, csuros_data)
        csuros_summary = summarize_errors(csuros_errors)

        # Calculate errors and summaries for Stream
        stream_errors = calculate_errors(exact_data, stream_data)
        stream_summary = summarize_errors(stream_errors)

        # Collect summaries for the file
        all_summaries.append({
            "filename": filename,
            "errors": {
                "Csuros Absolute Error": csuros_summary["absolute_error"],
                "Csuros Relative Error": csuros_summary["relative_error"],
                "Stream Absolute Error": stream_summary["absolute_error"],
                "Stream Relative Error": stream_summary["relative_error"],
            },
        })

    # Save all summaries to a single CSV
    output_csv = f"{GRAPHICS_DIR}/error_analysis_summary.csv"
    save_all_summaries_to_csv(all_summaries, output_csv)
    print(f"All error summaries saved to: {output_csv}")

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
    analyze_errors()