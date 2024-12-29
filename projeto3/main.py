from pathlib import Path
from src.counters.exact_counter import exact_counter_with_save
from src.counters.csuros_counter import csuros_counter_with_save
from src.counters.stream_counter import misra_gries_counter_with_save, verify_frequent_items

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
        filename = file_path.stem
        print(f"Analyzing '{filename}'...")

        # Load preprocessed text
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        # Exact Counter
        exact_counter_with_save(text, filename)

        # Csuros' Counter
        csuros_counter_with_save(text, filename, sampling_rate=0.1)

        # Stream Counter
        misra_gries_counter_with_save(text, filename)

if __name__ == "__main__":
    main()
