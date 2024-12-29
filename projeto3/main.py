import csv
import time
import tracemalloc
from pathlib import Path
from src.counters.exact_counter import exact_counter_with_save
from src.counters.csuros_counter import csuros_counter_with_save
from src.counters.stream_counter import misra_gries_counter_with_save, verify_frequent_items

# Directory for processed files
PROCESSED_DIR = "./data/processed/"
RESULTS_FILE = "./data/performance_metrics.csv"

def measure_performance(func, *args, **kwargs):
    """
    Measure the performance of a function.

    Args:
        func (callable): The function to measure.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.

    Returns:
        dict: A dictionary with execution time and memory usage.
    """
    # Start tracking memory
    tracemalloc.start()

    # Record start time
    start_time = time.perf_counter()

    # Execute the function
    func(*args, **kwargs)

    # Record end time
    end_time = time.perf_counter()

    # Get memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "execution_time": end_time - start_time,
        "memory_usage": peak / 1024,  # Convert to KB
    }

def save_performance_metrics(metrics):
    """
    Save performance metrics to a CSV file.

    Args:
        metrics (list): A list of dictionaries with performance metrics.
    """
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["filename", "algorithm", "execution_time", "memory_usage"])
        writer.writeheader()
        writer.writerows(metrics)

def main():
    """
    Run algorithms on preprocessed text files and record performance metrics.
    """
    processed_files = list(Path(PROCESSED_DIR).glob("*.txt"))
    if not processed_files:
        print("No processed files found. Please run `preprocess.py` first.")
        return

    metrics = []

    for file_path in processed_files:
        filename = file_path.stem
        print(f"Analyzing '{filename}'...")

        # Load preprocessed text
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Measure Exact Counter
        exact_perf = measure_performance(exact_counter_with_save, text, filename)
        exact_perf.update({"filename": filename, "algorithm": "Exact Counter"})
        metrics.append(exact_perf)

        # Measure Csuros' Counter
        csuros_perf = measure_performance(csuros_counter_with_save, text, filename, sampling_rate=0.1)
        csuros_perf.update({"filename": filename, "algorithm": "Csuros' Counter"})
        metrics.append(csuros_perf)

        # Measure Misra-Gries Counter
        mg_perf = measure_performance(misra_gries_counter_with_save, text, filename)
        mg_perf.update({"filename": filename, "algorithm": "Misra-Gries Counter"})
        metrics.append(mg_perf)

    # Save performance metrics to a CSV file
    save_performance_metrics(metrics)
    print(f"Performance metrics saved to '{RESULTS_FILE}'.")

if __name__ == "__main__":
    main()
