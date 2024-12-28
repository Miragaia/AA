from pathlib import Path

# Directory for processed files
PROCESSED_DIR = "./data/processed/"

def main():
    """
    Run algorithms using preprocessed data.
    """
    # Ensure the processed directory exists and contains files
    processed_files = list(Path(PROCESSED_DIR).glob("*.txt"))
    if not processed_files:
        print("No processed files found. Please run `preprocess.py` first.")
        return

    for file_path in processed_files:
        print(f"Running algorithms on '{file_path.name}'...")
        # Load cleaned text
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Call algorithms here (e.g., exact word count, approximate counters)
        # Placeholder for now
        print(f"Loaded {len(text.split())} words from '{file_path.name}'.")
        # TODO: Add exact word count and other counters here

if __name__ == "__main__":
    main()
