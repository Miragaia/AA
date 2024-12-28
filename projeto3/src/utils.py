import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
from pathlib import Path

# Pre-download NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def clean_text(text, language='english'):
    """
    Clean the input text by removing headers, tails, stopwords, punctuation, and converting to lowercase.

    Args:
        text (str): The text to be cleaned.
        language (str): The language for stopwords (default: 'english').

    Returns:
        str: The cleaned text.
    """
    # Load stopwords for the specified language
    try:
        stop_words = set(stopwords.words(language))
    except OSError:
        raise ValueError(f"Stop words for the language '{language}' are not available in NLTK.")

    # Remove Project Gutenberg headers/tails
    text = remove_gutenberg_headers(text)

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Convert to lowercase
    text = text.lower()

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Join back into a single string
    return ' '.join(filtered_tokens)

def remove_gutenberg_headers(text):
    """
    Remove headers and footers from Project Gutenberg texts.

    Args:
        text (str): The text to be processed.

    Returns:
        str: The text without headers and footers.
    """
    HEADER_MARKER = "*** START OF THE PROJECT GUTENBERG EBOOK"
    FOOTER_MARKER = "*** END OF THE PROJECT GUTENBERG EBOOK"

    # Remove content before the header
    if HEADER_MARKER in text:
        text = text.split(HEADER_MARKER, 1)[1]

    # Remove content after the footer
    if FOOTER_MARKER in text:
        text = text.split(FOOTER_MARKER, 1)[0]

    return text.strip()

def detect_language_from_filename(filename):
    """
    Detect the language based on the file name.

    Args:
        filename (str): The name of the file (e.g., 'book_english.txt').

    Returns:
        str: The detected language (e.g., 'english').
    """
    if 'english' in filename.lower():
        return 'english'
    elif 'french' in filename.lower():
        return 'french'
    elif 'german' in filename.lower():
        return 'german'
    elif 'spanish' in filename.lower():
        return 'spanish'
    else:
        raise ValueError(f"Language could not be detected from the filename '{filename}'.")

def save_results(results, filename, folder):
    """
    Save results to a JSON file.

    Args:
        results (dict): The results to save.
        filename (str): The name of the file (without extension).
        folder (str): The directory to save the file.
    """
    Path(folder).mkdir(parents=True, exist_ok=True)
    file_path = Path(folder) / f"{filename}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Results saved to {file_path}")