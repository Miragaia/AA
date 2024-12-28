from collections import Counter
from ..utils import save_results

def exact_counter(text):
    """
    Count exact word frequencies in the text.

    Args:
        text (str): The preprocessed text.

    Returns:
        dict: A dictionary with words as keys and their counts as values.
    """
    words = text.split()
    word_counts = Counter(words)
    return word_counts

def exact_counter_with_save(text, filename):
    """
    Count exact word frequencies and save results.

    Args:
        text (str): The preprocessed text.
        filename (str): The name of the output file (without extension).
    """
    results = exact_counter(text)
    save_results(results, filename, "./data/results/exact/")
    return results
