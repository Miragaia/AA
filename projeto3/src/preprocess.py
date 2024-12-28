from pathlib import Path
from utils import detect_language_from_filename, clean_text

# Directory for processed files
PROCESSED_DIR = "../data/processed/"
RAW_DIR = "../data/raw/"

def preprocess_files():
    """
    Preprocess all raw text files and save the cleaned versions.
    """
    for file_path in Path(RAW_DIR).glob("*.txt"):
        # Detect language from file name
        language = detect_language_from_filename(file_path.name)
        print(f"Processing '{file_path.name}' with language: {language}")

        # Read raw text
        with open(file_path, 'r', encoding='utf-8') as file:
            raw_text = file.read()

        # Clean the text
        cleaned_text = clean_text(raw_text, language=language)

        # Save the cleaned text
        cleaned_file_path =  Path(PROCESSED_DIR) / f"{file_path.stem}_cleaned.txt"
        with open(cleaned_file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_text)

        print(f"Saved cleaned text to '{cleaned_file_path}'.")

# Run preprocessing
if __name__ == "__main__":
    preprocess_files()
