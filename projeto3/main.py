from pathlib import Path
from src.counters.exact_counter import exact_counter
from src.counters.csuros_counter import csuros_counter
from src.counters.frequent_count import frequent_count

# Directory for processed files
PROCESSED_DIR = "./data/processed/"

def main():
    """
    Run algorithms on preprocessed text files.
    """
    processed_files = list(Path(PROCESSED_DIR).glob("*.txt"))
    if not processed_files:
        print("No processed files found. Please run `preprocess.py` first.")
        return

    for file_path in processed_files:
        print(f"Analyzing '{file_path.name}'...")
        
        # Load preprocessed text
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Exact Counter
        exact_results = exact_counter(text)
        print(f"Exact Counter: Top 5 words: {dict(sorted(exact_results.items(), key=lambda x: x[1], reverse=True)[:5])}")

        # Csuros' Counter
        csuros_results = csuros_counter(text, sampling_rate=0.1)
        print(f"Csuros' Counter: Top 5 estimated words: {dict(sorted(csuros_results.items(), key=lambda x: x[1], reverse=True)[:5])}")

        # Frequent-Count
        frequent_results = frequent_count(text, threshold=10)
        print(f"Frequent-Count: Words with count > 10: {list(frequent_results.keys())[:5]}")

        print("----------------------------------------------------")

if __name__ == "__main__":
    main()
